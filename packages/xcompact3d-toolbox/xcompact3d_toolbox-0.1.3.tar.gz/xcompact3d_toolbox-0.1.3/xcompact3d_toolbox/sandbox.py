"""
.. module:: sandbox
    :synopsis: Initializes and provides to the user all variables that are
               expected by Xcompact3d and the new sandbox flow configuration.
.. moduleauthor:: Felipe N. Schuch <felipe.schuch@edu.purcs.br>
"""

from .array import X3dDataArray, X3dDataset
from .mesh import get_mesh
from .param import param
import numpy as np
import os.path
import xarray as xr

def init_epsi(prm, dask=False):
    """Initilizes the arrays that defines the solid geometry that is going to be
    inserted into the Navier-Stokes solver.

    Parameters
    ----------
    prm : Class xcompact3d_toolbox.Parameters
        Contains the computational and physical parameters.
    dask : bool
        Defines the lazy parallel execution with dask arrays.
        See xarray.x3d.pencil_decomp().

    Returns
    -------
    dict
        A dictionary containing the epsi(s) array(s):
            - epsi (nx, ny, nz) if iibm != 0;
            - xepsi (nxraf, ny, nz) if iibm = 2;
            - yepsi (nx, nyraf, nz) if iibm = 2;
            - zepsi (nx, ny, nzraf) if iibm = 2.
        Each one initialized with np.zeros(dtype=np.bool) and wrapped into a
        xarray.DataArray with the proper size, dimensions and coordinates.
        They are used to define the object(s) that is(are) going to be inserted
        into the cartesiann domain by the Immersed Boundary Method (IBM).
        They should be set to one (True) at the solid points and stay
        zero (False) at the fluid points, some standard geometries are provided
        by the accessor xcompact3d_toolbox.sandbox.geo.
        Then, send them to xcompact3d_toolbox.gene_epsi_3d().

    """

    epsi = {}

    if prm.iibm == 0:
        return epsi

    from os import makedirs

    makedirs(os.path.join('data', 'geometry'), exist_ok=True)

    mesh = get_mesh(prm)

    # the epsi array in the standard mesh (nx, ny, nz)
    fields = {
        'epsi': (mesh['x'], mesh['y'], mesh['z'])
    }

    if prm.iibm == 2:
        # Getting refined mesh
        mesh_raf = get_mesh(prm, raf = True)
        # Three additional versions are needed if iibm = 2,
        # each one refined in one dimension by a factor nraf
        fields['xepsi'] = (mesh_raf['x'], mesh['y'], mesh['z'])
        fields['yepsi'] = (mesh['x'], mesh_raf['y'], mesh['z'])
        fields['zepsi'] = (mesh['x'], mesh['y'], mesh_raf['z'])

    # Data type defined to boolean for simplicity, since epsi should be zero at
    # the fluid points and one at the solid points. The algorithm should work
    # for integer ao float as well
    for key, (x, y, z) in fields.items():
        epsi[key] = xr.DataArray(
            np.zeros((x.size, y.size, z.size), dtype=np.bool),
            dims=['x', 'y', 'z'],
            coords={'x': x, 'y': y, 'z': z},
            name = key
        )

    # With 'file_name' attribute, we make sure that epsi will be written to disc,
    # while the refined versions are not needed
    epsi['epsi'].attrs={
        'file_name': os.path.join('data', 'geometry', 'epsilon')
    }

    # Turns on lazy parallel execution with dask arrays
    if dask == True:
        for key in epsi.keys():
            if key == 'epsi':
                # Decomposition in any direction would work for epsi
                epsi[key] = epsi[key].x3d.pencil_decomp('x')
            else:
                # notice that key[0] will be x, y and z for
                # xepsi, yepsi and zepsi, respectively
                epsi[key] = epsi[key].x3d.pencil_decomp(key[0])

    return epsi

def init_dataset(prm):
    """This function initializes a xarray.Dataset in addition to all variables
    that should be provided to Xcompact3d and the sandbox flow configuration,
    according to the provided computational and physical parameters.

    Parameters
    ----------
    prm : Class xcompact3d_toolbox.Parameters
        Contains the computational and physical parameters.

    Returns
    -------
    xarray.Dataset
        Each variable is initialized with
        np.zeros(dtype=xcompact3d_toolbox.param['mytype']) and wrapped into a
        xarray.Dataset with the proper size, dimensions, coordinates and
        attributes, check them for more details. The variables are:
            - bxx1, bxy1, bxz1: Inflow boundary condition for ux, uy and uz,
              respectively (if nclx1 = 2);
            - bxphi1: Inflow boundary condition for scalar field(s)
              (if nclx1 = 2 and numscalar > 0);
            - byphi1: Bottom boundary condition for scalar field(s)
              (if nclyS1 = 2, numscalar > 0 and uset = 0);
            - byphin: Top boundary condition for scalar field(s)
              (if nclySn = 2, numscalar > 0 and uset = 0);
            - ux, uy, uz: Initial condition for velocity field;
            - phi: Initial condition for scalar field(s) (if numscalar > 0);
            - vol_frc: Integral operator employed for flow rate control in case
              of periodicity in x direction (nclx1 = 0 and nclxn = 0).
              Xcompact3d will compute the volumetric integration as
              I = sum(vol_frc * ux) and them will correct streamwise velocity
              as ux = ux / I, so, set vol_frc properly.
        After setting all values for your flow configuration, the dataset can be
        written to disc with xarray.Dataset.x3d.write().

    """

    from os import makedirs

    makedirs(os.path.join('data'), exist_ok=True)

    #Init dataset
    ds = xr.Dataset(coords=get_mesh(prm)).assign_coords(
        {'n': range(prm.numscalar)}
    )

    ds.x.attrs = {'name': 'Streamwise coordinate', 'long_name': r'$x_1$'}
    ds.y.attrs = {'name': 'Vertical coordinate', 'long_name': r'$x_2$'}
    ds.z.attrs = {'name': 'Spanwise coordinate', 'long_name': r'$x_3$'}
    ds.n.attrs = {'name': 'Scalar fraction', 'long_name': r'$\ell$'}

    #Boundary conditions
    if prm.nclx1 == 2:
        for var in 'bxx1 bxy1 bxz1 noise_mod_x1'.split():
            ds[var] = xr.DataArray(
                param['mytype'](0.0),
                dims=['y', 'z'],
                coords=[ds.y, ds.z],
                attrs={
                    'file_name': os.path.join('data', var)
                }
            )
    if prm.numscalar != 0:
        if prm.nclxS1 == 2:
            ds['bxphi1'] = xr.DataArray(
                param['mytype'](0.0),
                dims=['n', 'y', 'z'],
                coords=[ds.n, ds.y, ds.z],
                attrs={
                    'file_name': os.path.join('data', 'bxphi1')
                }
            )
        if prm.nclyS1 == 2:
            ds['byphi1'] = xr.DataArray(
                param['mytype'](0.0),
                dims=['n', 'x', 'z'],
                coords=[ds.n, ds.x, ds.z],
                attrs={
                    'file_name': os.path.join('data', 'byphi1')
                }
            )
        if prm.nclySn == 2:
            ds['byphin'] = xr.DataArray(
                param['mytype'](0.0),
                dims=['n', 'x', 'z'],
                coords=[ds.n, ds.x, ds.z],
                attrs={
                    'file_name': os.path.join('data', 'byphin')
                }
            )
    #Initial Condition
    for var in ['ux', 'uy', 'uz']:
        ds[var] = xr.DataArray(
            param['mytype'](0.0),
            dims=['x', 'y', 'z'],
            coords=[ds.x, ds.y, ds.z],
            attrs={
                'file_name': os.path.join('data', var)
            }
        )
    if prm.numscalar != 0:
        ds['phi'] = xr.DataArray(
            param['mytype'](0.0),
            dims=['n', 'x', 'y', 'z'],
            coords=[ds.n, ds.x, ds.y, ds.z],
            attrs={
                'file_name': os.path.join('data', 'phi')
            }
        )
    # Flowrate control
    if prm.nclx1 == 0 and prm.nclxn == 0:
        ds['vol_frc'] = xr.DataArray(
            param['mytype'](0.0),
            dims=['x', 'y', 'z'],
            coords=[ds.x, ds.y, ds.z],
            attrs={
                'file_name': os.path.join('data', 'vol_frc')
            }
        )

    return ds

@xr.register_dataarray_accessor("geo")
class Geometry:
    def __init__(self, data_array):
        self._data_array = data_array

    def cylinder(self, center=dict(x=0, y=0, z=0), r=0.5, axis='z', height=None, remp=True):

        dis = 0.0
        for d in self._data_array.dims:
            if d == axis:
                continue
            dis = dis + (self._data_array[d] - center[d])**2.0
        dis = np.sqrt(dis)

        if height != None:
            height /= 2.
            # Notice that r*10 is just to garantee that the values are larger than r
            # and consequently outside the cylinder
            dis = dis.where(self._data_array[axis] <= center[axis] + height, r*10)
            dis = dis.where(self._data_array[axis] >= center[axis] - height, r*10)

        return self._data_array.where(dis > r, remp)

    def box(self, remp=True, **boundaries):

        for key in boundaries.keys():
            if not key in self._data_array.dims:
                raise KeyError(f'Invalid key for "boundaries", it should be a valid dimension')

        tmp = xr.zeros_like(self._data_array)

        for key, value in boundaries.items():
            tmp = tmp.where(self._data_array[key] >= value[0], True)
            tmp = tmp.where(self._data_array[key] <= value[1], True)

        return self._data_array.where(tmp, remp)

    def square(self, center=dict(x=0, y=0, z=0), length=1.0, thickness=0.1, remp=True):
        boundaries1 = {
            'x': (center['x'] - 0.5 * thickness, center['x'] + 0.5 * thickness),
            'y': (center['y'] - 0.5 * length, center['y'] + 0.5 * length),
            'z': (center['z'] - 0.5 * length, center['z'] + 0.5 * length)
        }
        tmp = self._data_array.geo.box(**boundaries1, remp=True)
        #
        length -= 2 * thickness
        boundaries2 = {
            'x': (center['x'] - 0.5 * thickness, center['x'] + 0.5 * thickness),
            'y': (center['y'] - 0.5 * length, center['y'] + 0.5 * length),
            'z': (center['z'] - 0.5 * length, center['z'] + 0.5 * length)
        }
        tmp = tmp.geo.box(**boundaries2, remp=False)
        #
        return self._data_array.where(tmp, remp)

    def sphere(self, center=dict(x=0, y=0, z=0), r=0.5, remp=True):

        dis = 0.0
        for d in self._data_array.dims:
            dis = dis + (self._data_array[d] - center[d])**2.0
        dis = np.sqrt(dis)

        return self._data_array.where(dis > r, remp)

    def ahmed_body(self, scale=1, angle=45.0, wheels=False, remp=True, **pos):

        import math

        s=scale/338 # adimensional and scale factor

        for key in pos.keys():
            if not key in self._data_array.dims:
                raise KeyError(f'Invalid key for "pos", it should be a valid dimension')

        if not 'x' in pos:
            pos['x'] = 1.0
        if not 'y' in pos:
            pos['y'] = 0.0
        if not 'z' in pos:
            pos['z'] = 0.5 * self._data_array.z[-1].values - ((389*s) / 2)
        else:
            # That is because of the mirror in Z
            raise NotImplementedError(
                    "Unsupported: Body should be centered in Z")

        if scale != 1:
            raise NotImplementedError(
            "Unsupported: Not prepared yet for scale != 1")

        tmp = xr.zeros_like(self._data_array)
        tmp2 = xr.zeros_like(self._data_array)


        # the "corners" are the intersections between the cylinders

        # horizontal

        tmp = tmp.geo.cylinder(center={
            'x': 100.00*s + pos['x'],
            'y': 150.00*s + pos['y'],
            'z':  97.25*s + pos['z']
        },
            axis='z',
            r=100.00*s,
            height=194.50*s)


        tmp = tmp.geo.cylinder(center={
            'x': 100.00*s + pos['x'],
            'y': 238.00*s + pos['y'],
            'z':  97.25*s + pos['z']
        },
            axis='z',
            r=100.00*s,
            height=194.50*s)

        #vertical

        tmp2 = tmp2.geo.cylinder(
            center={
                'x': 100.00*s + pos['x'],
                'y': 194.00*s + pos['y'],
                'z': 100.00*s + pos['z']
            },
            axis='y',
            r=100.00*s,
            height=288.00*s)

        # get intersection
        tmp = np.logical_and(tmp == True, tmp2 == True)

        del tmp2

        # now the regular cylinders

        tmp = tmp.geo.cylinder(center={
            'x': 100.00*s + pos['x'],
            'y': 150.00*s + pos['y'],
            'z': 147.25*s + pos['z']
        },
            axis='z',
            r=100.00*s,
            height=94.50*s)

        tmp = tmp.geo.cylinder(center={
            'x': 100.00*s + pos['x'],
            'y': 238.00*s + pos['y'],
            'z': 147.25*s + pos['z']
        },
            axis='z',
            r=100.00*s,
            height=94.50*s)

        tmp = tmp.geo.cylinder(center={
            'x': 100.00*s + pos['x'],
            'y': 194.00*s + pos['y'],
            'z': 100.00*s + pos['z']
        },
            axis='y',
            r=100.00*s,
            height=88.00*s)

        if wheels:
            tmp = tmp.geo.cylinder(center={
                'x': 200.00*s + pos['x'],
                'y':  25.00*s + pos['y'],
                'z':  46.50*s + pos['z']
            },
                axis='y',
                r=15.00*s,
                height=50.00*s)

            tmp = tmp.geo.cylinder(center={
                'x': 725.00*s + pos['x'],
                'y':  25.00*s + pos['y'],
                'z':  46.50*s + pos['z']
            },
                axis='y',
                r=15.00*s,
                height=50.00*s)

        # the boxes
        tmp = tmp.geo.box(x=(           pos['x'],  200.00*s + pos['x']),
                          y=(150.00*s + pos['y'],  238.00*s + pos['y']),
                          z=(100.00*s + pos['z'],  194.50*s + pos['z']))

        tmp = tmp.geo.box(x=(100.00*s + pos['x'], 1044.00*s + pos['x']),
                          y=( 50.00*s + pos['y'],  338.00*s + pos['y']),
                          z=(           pos['z'],  194.50*s + pos['z'] ))

        # and finally a mirror
        tmp = tmp.geo.mirror(dim='z')

        # Angle in the back
        hipo=(93.80/math.sin(math.radians(25)))*s
        adj = math.cos(math.radians(angle)) * hipo
        opo = math.sin(math.radians(angle)) * hipo

        x = [1044.00*s - adj + pos['x'], 1044.00*s       + pos['x']]
        y = [ 338.00*s       + pos['y'],  338.00*s - opo + pos['y']]

        coef = np.polyfit(x, y, 1)

        cut = self._data_array.x * coef[0] + coef[1]

        tmp = tmp.where(self._data_array.y <= cut, False)

        return self._data_array.where(np.logical_not(tmp), remp)

    def mirror(self, dim='x'):
        return self._data_array.where(
            self._data_array[dim] <= self._data_array[dim][-1]/2., self._data_array[{
                dim: slice(None, None, -1)
            }].values)

    def visual3d(self):

        import plotly.graph_objects as go
        import plotly.offline as pyo
        import plotly.io as pio

        pio.renderers.default = 'browser' #'jupyterlab', 'vscode', 'nteract', 'notebook_connected', 'png', 'jpeg', 'jpg', 'svg', 'pdf', 'browser', 'sphinx_gallery'

        X, Y, Z = np.mgrid[0:self._data_array.x[-1].values:self._data_array.x.shape[0]*1j,
                           0:self._data_array.y[-1].values:self._data_array.y.shape[0]*1j,
                           0:self._data_array.z[-1].values:self._data_array.z.shape[0]*1j]

        values = (self._data_array*1).values

        fig = go.Figure()

        #fig.add_scatter3d(x=X.flatten(), y=Y.flatten(), z=Z.flatten(), mode='markers',marker=dict(size=0.75))

        fig.add_isosurface(x=X.flatten(),
                           z=Y.flatten(),
                           y=Z.flatten(),
                           value=values.flatten(),
                           isomin=0.99,
                           isomax=1,
                           colorscale='sunset',
                           lighting=dict(ambient=0.4,
                                         specular=1.0))

        fig.update_layout(scene_aspectmode='data')
        fig.update_traces(showscale=False)

        fig.show()
