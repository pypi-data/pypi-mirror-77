import torch
import molgrid as mg
import types
def tensor_as_grid(t):
    '''Return a Grid view of tensor t'''
    gname = 'Grid'
    gname += str(t.dim())
    g = globals()
    if isinstance(t,torch.FloatTensor):
        gname += 'f'
        return getattr(mg,gname)(mg.tofloatptr(t.data_ptr()),*t.shape)
    elif isinstance(t,torch.DoubleTensor):
        gname += 'd'
        return getattr(mg,gname)(mg.todoubleptr(t.data_ptr()),*t.shape)
    elif isinstance(t,torch.cuda.FloatTensor):
        gname += 'fCUDA'
        return getattr(mg,gname)(mg.tofloatptr(t.data_ptr()),*t.shape)
    elif isinstance(t,torch.cuda.DoubleTensor):
        gname += 'dCUDA'
        return getattr(mg,gname)(mg.todoubleptr(t.data_ptr()),*t.shape)    
    else:
        raise ValueError('Tensor base type %s not supported as grid type.'%str(t.dtype))
    
    return t

#extend grid maker to create pytorch Tensor
def make_grid_tensor(gridmaker, center, c):
    '''Create appropriately sized pytorch tensor of grid densities.  set_gpu_enabled can be used to control if result is located on the cpu or gpu'''
    dims = gridmaker.grid_dimensions(c.max_type) # this should be grid_dims or get_grid_dims
    if mg.get_gpu_enabled():
        t = torch.zeros(dims, dtype=torch.float32, device='cuda:0')
    else:
        t = torch.zeros(dims, dtype=torch.float32)
    gridmaker.forward(center, c, t)
    return t 

mg.GridMaker.make_tensor = make_grid_tensor
    
class Grid2CoordsGradientFunction(torch.autograd.Function):
    '''Backwards pass of grid generation so can create graph of gradient calculation'''
    
    @staticmethod
    def forward(ctx, gmaker, center, coords, types, radii, grid_gradient):
        '''Return Nx3 coordinate gradient and NxT type gradient'''
        ctx.save_for_backward(coords, types, radii, grid_gradient)
        ctx.gmaker = gmaker
        ctx.center = center
        grad_coords = torch.empty(*coords.shape,dtype=coords.dtype,device=coords.device)
        grad_types = torch.empty(*types.shape,dtype=types.dtype,device=types.device)
        #radii are fixed
        gmaker.backward(center, coords, types, radii, grid_gradient, grad_coords, grad_types)
        return grad_coords, grad_types
        
    @staticmethod
    def backward(ctx, grad_coords, grad_types):
        '''Return second order grid gradient'''
        coords, types, radii, grid_gradient = ctx.saved_tensors
        gmaker = ctx.gmaker
        center = ctx.center
                
        ddcoords = torch.empty(*coords.shape,dtype=coords.dtype,device=coords.device)
        ddtypes = torch.empty(*types.shape,dtype=types.dtype,device=types.device)
        ddG = torch.empty(*grid_gradient.shape,dtype=grid_gradient.dtype,device=grid_gradient.device)
        
        gmaker.backward_gradients(center, coords, types, radii, grid_gradient, grad_coords, grad_types, ddG, ddcoords, ddtypes)

        return None, None, ddcoords, ddtypes, None, ddG 
    
class Coords2GridFunction(torch.autograd.Function):
    '''Layer for converting from coordinate and type tensors to a molecular grid'''
    
    @staticmethod
    def forward(ctx, gmaker, center, coords, types, radii):
        '''coords are Nx3, types are NxT, radii are N'''
        ctx.save_for_backward(coords, types, radii)
        ctx.gmaker = gmaker
        ctx.center = center
        shape = gmaker.grid_dimensions(types.shape[1]) #ntypes == nchannels
        output = torch.empty(*shape,dtype=coords.dtype,device=coords.device)
        gmaker.forward(center, coords, types, radii, output)
        return output
        
    @staticmethod
    def backward(ctx, grid_gradient):
        '''Return Nx3 coordinate gradient and NxT type gradient'''
        coords, types, radii = ctx.saved_tensors
        gmaker = ctx.gmaker
        center = ctx.center

        #radii are fixed
        grad_coords, grad_types = Grid2CoordsGradientFunction.apply(gmaker, center, coords, types, radii, grid_gradient)
        return None, None, grad_coords, grad_types, None
            
        
class BatchedCoords2GridFunction(torch.autograd.Function):
    '''Layer for converting from coordinate and type tensors to a molecular grid using batched input'''
    
    @staticmethod
    def forward(ctx, gmaker, center, coords, types, radii):
        '''coords are Nx3, types are NxT, radii are N'''
        ctx.save_for_backward(coords, types, radii)
        ctx.gmaker = gmaker
        ctx.center = center
        batch_size = coords.shape[0]
        if batch_size != types.shape[0] or batch_size != radii.shape[0]:
            raise RuntimeError("Inconsistent batch sizes in Coords2Grid inputs")
        shape = gmaker.grid_dimensions(types.shape[2]) #ntypes == nchannels
        output = torch.empty(batch_size,*shape,dtype=coords.dtype,device=coords.device)
        for i in range(batch_size):
            gmaker.forward(center, coords[i], types[i], radii[i], output[i])
        return output
        
    @staticmethod
    def backward(ctx, grid_gradient):
        '''Return Nx3 coordinate gradient and NxT type gradient'''
        coords, types, radii = ctx.saved_tensors
        gmaker = ctx.gmaker
        center = ctx.center
        grad_coords = torch.empty(*coords.shape,dtype=coords.dtype,device=coords.device)
        grad_types = torch.empty(*types.shape,dtype=types.dtype,device=types.device)
        #radii are fixed
        batch_size = coords.shape[0]
        for i in range(batch_size):
            gmaker.backward(center, coords[i], types[i], radii[i], grid_gradient[i], grad_coords[i], grad_types[i])
        return None, None, grad_coords, grad_types, None
            
class Coords2Grid(torch.nn.Module):
    def __init__(self, gmaker, center=(0,0,0)):
        '''Convert coordinates/types/radii to a grid using the provided
        GridMaker and grid center'''
        super(Coords2Grid, self).__init__()
        self.gmaker = gmaker
        self.center = center
        
    def forward(self, coords, types, radii):
        if not coords.is_contiguous():
            coords = coords.clone()
        if not types.is_contiguous():
            types = types.clone()
        if not radii.is_contiguous():
            radii == radii.clone()
        if len(coords.shape) == 3 and len(types.shape) == 3 and len(radii.shape) == 2: #batched
            return BatchedCoords2GridFunction.apply(self.gmaker, self.center, coords, types, radii)
        elif len(coords.shape) == 2 and len(types.shape) == 2 and len(radii.shape) == 1:
            return Coords2GridFunction.apply(self.gmaker, self.center, coords, types, radii)
        else:
            raise RuntimeError("Invalid input dimensions in forward of Coords2Grid")
    
    def extra_repr(self):
        return 'resolution {:.2f}, dimension {}, center {:.3f},{:.3f},{:.3f}'.format(
                self.gmaker.get_resolution(), self.gmaker.get_dimension(), self.center[0], self.center[1], self.center[2])        
