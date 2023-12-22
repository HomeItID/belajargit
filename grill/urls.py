from django.urls import path
from . import views

urlpatterns = [
    path('home',views.home,name='home'),

    #login
    path('', views.loginview , name='login'),
    path('performlogin', views.performlogin, name='performlogin'),
    path('performlogout', views.performlogout , name='performlogout'),

    #Karyawan
    path('karyawan',views.karyawan,name='karyawan'),
    path('ckaryawan',views.ckaryawan,name='ckaryawan'),
    path('ukaryawan/<str:id>',views.ukaryawan,name='ukaryawan'),
    path('dkaryawan/<str:id>',views.dkaryawan,name='dkaryawan'),

    #jenis_pengiriman
    path('jenis_pengiriman',views.jenis_pengiriman,name='jenis_pengiriman'),
    path('cjenis_pengiriman',views.cjenis_pengiriman,name='cjenis_pengiriman'),
    path('ujenis_pengiriman/<str:id>',views.ujenis_pengiriman,name='ujenis_pengiriman'),
    path('djenis_pengiriman/<str:id>',views.djenis_pengiriman,name='djenis_pengiriman'),

    #paket
    path('paket',views.paket,name='paket'),
    path('cpaket',views.cpaket,name='cpaket'),
    path('upaket/<str:id>',views.upaket,name='upaket'),
    path('dpaket/<str:id>',views.dpaket,name='dpaket'),

    
    #pelanggan
    path('pelanggan',views.pelanggan,name='pelanggan'),
    path('cpelanggan',views.cpelanggan,name='cpelanggan'),
    path('upelanggan/<str:id>',views.upelanggan,name='upelanggan'),
    path('dpelanggan/<str:id>',views.dpelanggan,name='dpelanggan'),

    #pelanggan
    path('pelanggan',views.pelanggan,name='pelanggan'),
    path('cpelanggan',views.cpelanggan,name='cpelanggan'),
    path('upelanggan/<str:id>',views.upelanggan,name='upelanggan'),
    path('dpelanggan/<str:id>',views.dpelanggan,name='dpelanggan'),

    #pemesanan
    path('pemesanan',views.pemesanan,name='pemesanan'),
    path('cpemesanan',views.cpemesanan, name='cpemesanan'),
    path('upemesanan/<str:id>',views.upemesanan,name='upemesanan'),
    path('dpemesanan/<str:id>',views.dpemesanan,name='dpemesanan'),

    #pengiriman
    path('pengiriman',views.pengiriman,name='pengiriman'),
    path('cpengiriman/<str:id>',views.cpengiriman, name='cpengiriman'),
    path('upengiriman/<str:id>',views.upengiriman,name='upengiriman'),
    path('dpengiriman/<str:id>',views.dpengiriman,name='dpengiriman'),

  #detail_pemesanan
    path('detail_pemesanan',views.detail_pemesanan,name='detail_pemesanan'),
    path('cdetail_pemesanan',views.cdetail_pemesanan, name='cdetail_pemesanan'),
    path('ddetail_pemesanan/<str:id>',views.ddetail_pemesanan,name='ddetail_pemesanan'),

  # Laporan
    path('laporan',views.laporanpemesanan, name='laporan'),
    path('laporanpdf/<str:mulai>/<str:akhir>',views.laporanpdf, name='laporanpdf')
    ]
     