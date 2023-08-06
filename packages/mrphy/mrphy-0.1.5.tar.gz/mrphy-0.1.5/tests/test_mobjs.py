import numpy as np
import torch
import pytest
from torch import tensor, cuda

from mrphy import γH, dt0, π, _slice
from mrphy import mobjs

# TODO:
# unit_tests for objects `.to()` methods


class Test_mobjs:

    device = torch.device('cuda' if cuda.is_available() else 'cpu')
    # device = torch.device('cpu')
    dtype, atol = torch.float32, 1e-4
    # dtype, atol = torch.float64, 1e-9
    print(device)

    dkw = {'dtype': dtype, 'device': device}

    γ = γH.to(**dkw)  # Hz/Gauss
    dt = dt0.to(**dkw)  # Sec

    @staticmethod
    def np(x):
        return x.detach().cpu().numpy()

    def test_Examples(self):
        ''' for coverage :/ '''
        assert(isinstance(mobjs.Examples.pulse(), mobjs.Pulse))
        assert(isinstance(mobjs.Examples.spincube(), mobjs.SpinCube))
        return

    def test_mobjs(self):
        kw, atol = self.dkw, self.atol
        γ, dt = self.γ, dt0  # For test coverage, not using self.dt here.

        N, Nd, nT = 1, (3, 3, 3), 512
        nT = 512

        # pulse: Sec; Gauss; Gauss/cm.
        pulse_size = (N, 1, nT)
        t = torch.arange(0, nT, **kw).reshape(pulse_size)
        rf = 10*torch.cat([torch.cos(t/nT*2*π),                # (1,xy, nT)
                           torch.sin(t/nT*2*π)], 1)
        gr = torch.cat([torch.ones(pulse_size, **kw),
                        torch.ones(pulse_size, **kw),
                        10*torch.atan(t - round(nT/2))/π], 1)  # (1,xyz,nT)

        # Pulse
        p = mobjs.Pulse(rf=rf, gr=gr, dt=dt, **kw)
        assert(p.is_cuda == (p.device.type == 'cuda'))
        p = mobjs.Pulse(**(p.asdict(toNumpy=False)))

        # SpinCube (SpinArray is implicitly tested via it)
        shape = (N, *Nd)
        mask = torch.zeros((1,)+Nd, device=self.device, dtype=torch.bool)
        mask[0, :, 1, :], mask[0, 1, :, :] = True, True
        fov, ofst = tensor([[3., 3., 3.]], **kw), tensor([[0., 0., 1.]], **kw)
        T1_, T2 = tensor([[1.]], **kw), tensor([[4e-2]], **kw)

        cube = mobjs.SpinCube(shape, fov, mask=mask, T1_=T1_, γ=γ, **kw)
        assert(cube.is_cuda == (cube.device.type == 'cuda'))
        cube_dict = cube.asdict(toNumpy=False)
        cube = mobjs.SpinCube(**{k: cube_dict[k] for
                                 k in ('shape', 'fov', 'mask', 'T1', 'γ'
                                       )+tuple(kw.keys())})
        cube.ofst = ofst  # separated for test coverage

        cube.M_ = tensor([0., 1., 0.])
        assert(cube.dim() == len(shape))
        cube.T2 = T2.expand(cube.shape)  # for test coverage

        M001, M100 = tensor([0., 0., 1.], **kw), tensor([1., 0., 0.], **kw)
        crds_100 = cube.crds_([_slice, [0, 1], [1, 0], _slice, _slice])
        cube.M_[crds_100] = M100
        crds_001 = cube.crds_([_slice, [2, 1], [1, 2], _slice, _slice])
        cube.M_[crds_001] = M001

        # gr_x/gr_y == 1 Gauss/cm cancels Δf[1, :, 0]/[1, 0, :] respectively
        loc = cube.loc

        cube.Δf = torch.sum(-loc[0:1, :, :, :, 0:2], dim=-1) * γ

        Mres1a = cube.applypulse(p, doEmbed=True)
        Mres1b = cube.applypulse(p, doEmbed=True, doRelax=False)

        # assertion
        Mo0a = np.array(
            [[[0.559535641648385,  0.663342640621335, 0.416341441715101],
              [0.391994737048090,  0.210182892388552, -0.860954821972489],
              [-0.677062008711222, 0.673391604920576, -0.143262993311057]]])

        Mo0b = np.array(
            [[[0.584337330324116,  0.686096989146395, 0.433382978292808],
              [0.404188676945936,  0.217027890590635, -0.888555236400348],
              [-0.703691265981316, 0.694384487290747, -0.150495136106067]]])

        Mrefa = pytest.approx(Mo0a, abs=atol)
        Mrefb = pytest.approx(Mo0b, abs=atol)

        assert(self.np(Mres1a[0:1, 1, :, 1, :]) == Mrefa)
        assert(self.np(Mres1a[0:1, :, 1, 1, :]) == Mrefa)

        assert(self.np(Mres1b[0:1, 1, :, 1, :]) == Mrefb)
        assert(self.np(Mres1b[0:1, :, 1, 1, :]) == Mrefb)

        return


if __name__ == '__main__':
    tmp = Test_mobjs()
    tmp.test_mobjs()
