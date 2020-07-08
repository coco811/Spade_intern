
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import seaborn as sea

class cross_section():
    def __init__(self, temp, topo, Gz):
        self.Gz=Gz
        self.topo=topo
        self.temp=temp
        self.dist_km=np.linspace(0,460,len(topo))

    def plot(self):
        fig, ax = plt.subplots(figsize=(15, 4), dpi=300, facecolor='white')
        ax.set_title('Vertical cross-section (3-km resolution): Topography', loc='left', fontsize=10)
        ax.plot(self.dist_km, self.topo, color='darkgrey', linewidth=2)
        ax.fill_between(self.dist_km, self.topo, color='grey', alpha=.35)

        cn = plt.tricontourf(self.Gz[0,0], self.temp[0], cmap='coolwarm',)
        colorbar = plt.colorbar(cn, ax=ax, pad=0.05, aspect=50, shrink=.75, extend='Max')
        colorbar.set_label('Temperature [\u2103]', rotation=270, fontsize=10, labelpad=11)
        colorbar.ax.tick_params(labelsize=7)

        ax.set_ylim(0, 4000)
        ax.set_xlim(self.dist_km[0], self.dist_km[-1])
        ax.set_xlabel('Distance (km)')
        ax.set_ylabel('Elevation (m)')
        ax.grid()
        ax.text(self.dist_km[0], -500, 'Nipika', va='center', ha='center', fontsize=16)
        ax.text(self.dist_km[-1], -500, 'Fortress', va='center', ha='center', fontsize=16)
        plt.show()



    def __call__(self):
        self.plot()

def intrp1d(varin, z, ztype, zref):
    nz = len(z)
    end = False
    varout=0
    if ztype == "Z":
        for k in range(nz):
            if ((z[k].any() >= zref) and (not end)):
                varout = varin[k] - (varin[k] - varin[k - 1]) / (z[k] - z[k - 1]) * (z[k] - zref)
                end = True
                break
    if ztype == "P":
        p = z
        pref = zref
        for k in range(nz):
            if ((p[k] <= pref) and (not end)):
                varout = varin[k] - (varin[k] - varin[k - 1]) / (p[k] - p[k - 1]) * (p[k] - pref)
                end = True
                break
    return varout

if __name__ == '__main__':
    temp = np.load('./Cross_section_data/Cross_section_460_1km/June_21_2019_storm/Variables/TT_array.npy')
    Gz=np.load('./Cross_section_data/Cross_section_460_1km/June_21_2019_storm/Variables/GZ_array.npy')* 10
    topo=np.load('./Cross_section_data/Cross_section_460_1km/June_21_2019_storm/Constants/transect_elevation.npy')

    ndat=np.shape(Gz)[0]
    Zmax = 35000.  # La hauteur maximale de l'interpolation

    nz = np.shape(Gz)[1]
    dZ = Zmax/nz
    distance= np.shape(Gz)[2]

    # Declaration des variables interpolee
    T_interp = np.zeros((nz,distance))
    # print(np.shape(T_interp))
    # print(np.shape(temp))
    Z_interp = np.linspace(0,Zmax, nz)

    for k in range(nz):
        for i in range(distance):
            T_interp[k,i] = intrp1d(temp[0, :,i], Gz[0,:, i], "Z", Z_interp[k])
    print(T_interp)
    # cross_section(temp,topo,Gz).plot()