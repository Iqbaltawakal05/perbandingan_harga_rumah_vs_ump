import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import process

def visualization(dataframe, dataApa, topik):        
    df_plot = dataframe.sort_values('mean', ascending=False)
    
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.vlines(x=df_plot[dataApa], 
            ymin=df_plot['min'], 
            ymax=df_plot['max'], 
            color='grey', 
            alpha=0.5, 
            linewidth=2, 
            label='Rentang Harga (Min-Max)')

    ax.scatter(df_plot[dataApa], 
            df_plot['mean'], 
            color='red', 
            s=50, 
            zorder=3, 
            label='Rata-rata (Mean)')

    ax.scatter(df_plot[dataApa], df_plot['min'], color='blue', s=10, marker='_')
    ax.scatter(df_plot[dataApa], df_plot['max'], color='blue', s=10, marker='_')
    
    ax.set_yscale('log')
    ax.set_title(f'Rentang & Rata-rata {topik.capitalize()} per {dataApa.capitalize()}', fontsize=14, fontweight='bold')
    ax.set_ylabel(topik.capitalize(), fontsize=12)
    ax.set_xlabel(dataApa, fontsize=12)

    def currency_formatter(x, pos):
        if x >= 1e9:
            return f'{x*1e-9:.0f} M'
        elif x >= 1e6:
            return f'{x*1e-6:.0f} Jt'
        else:
            return f'{x:.0f}'

    def tahun_formatter(x, pos):
        return f"{int(x):,} Tahun"
    
    if topik.lower() == "harga rumah":
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(currency_formatter))
    else:
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(tahun_formatter))

        text_str = "Catatan:\n- Asumsi menabung pada data UMP tahun 2020"
        ax.text(1.02, 0.95, text_str, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    
    plt.xticks(rotation=90)
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.legend()

    plt.tight_layout()
    return fig
    
def plotBar(datanya):
    datanya = datanya.sort_values('UpahMinimum', ascending=False)
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.bar(datanya['Provinsi'], datanya['UpahMinimum'], color='red')
    ax.set_title('Upah Minimum per Provinsi', fontsize=14, fontweight='bold')
    ax.set_xlabel('Provinsi', fontsize=12)
    ax.set_ylabel('Upah Minimum (Juta)', fontsize=12)
    
    def currency_formatter(x, pos):
        return f"{int(x):,} Jt"
    
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(currency_formatter))
    
    plt.xticks(rotation=90)
    plt.tight_layout()
    
    return fig
    
def main():
    dataMateng = process.main()
    hargaProv = dataMateng['hargaStatPerProv']
    lamaProv = dataMateng['lamaMenabungStatPerProv']
    hargaKab = dataMateng['hargastatPerKab']
    lamaKab = dataMateng['lamaMenabungStatPerKab']
    dataUMP = dataMateng['dataUMP2020']
    
    return {
        'hargaStatPerProv': visualization(hargaProv, dataApa='provinsi', topik='Harga Rumah'),
        'lamaMenabungStatPerProv': visualization(lamaProv, dataApa='provinsi', topik='lama menabung'),
        'hargastatPerKab': visualization(hargaKab, dataApa='kabupaten', topik='Harga Rumah'),
        'lamaMenabungStatPerKab': visualization(lamaKab, dataApa='kabupaten', topik='lama menabung'),
        'dataUMP2020': plotBar(dataUMP)
    }

if __name__ == "__main__":
    print("file ini tidak bisa dijalankan secara langsung, silahkan import sebagai module")
