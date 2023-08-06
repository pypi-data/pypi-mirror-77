# -*- coding: utf-8 -*-


def comp_volume_magnets(self):
    """Compute the volume of the hole magnets

    Parameters
    ----------
    self : HoleM50
        A HoleM50 object

    Returns
    -------
    Vmag: float
        Volume of the 2 Magnets [m**3]

    """

    V = 0
    if self.magnet_0:
        V += self.H3 * self.W4 * self.magnet_0.Lmag
    if self.magnet_1:
        V += self.H3 * self.W4 * self.magnet_1.Lmag
    return V
