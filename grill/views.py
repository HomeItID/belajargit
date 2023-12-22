from django.shortcuts import render, redirect
from . import models
from datetime import datetime, date, timedelta
import calendar
from .decorators import role_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login , logout, authenticate
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.forms import DateInput
from django.db import transaction
from django.core.exceptions import ValidationError
import json
from weasyprint import HTML
from django.template.loader import render_to_string
import tempfile
from django.db.models import Sum
import numpy as np

print("hellooooo ini im eldaaa")
print("hellooooo ini im eldaaa")
print("hellooooo ini im eldaaa")
print("hellooooo ini im eldaaa")
print("hellooooo ini im eldaaa")
print("hellooooo ini im eldaaa")
print("hellooooo ini im eldaaa")
print("hellooooo ini im eldaaa")


# Create your views here.

#  LOGIN
@login_required(login_url="login")
def logoutview(request):
    logout(request)
    messages.info(request,"Berhasil Logout")
    return redirect('login')

def loginview(request):
    if request.user.is_authenticated:
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group in ['admin', 'owner']:
            return redirect('home')
    else:
        return render(request,"logins/login.html")

def performlogin(request):
    if request.method != "POST":
        return HttpResponse("Method not Allowed")
    else:
        username_login = request.POST['username']
        password_login = request.POST['password']
        userobj = authenticate(request, username=username_login,password=password_login)
        if userobj is not None:
            login(request, userobj)
            messages.success(request,"Login success")

            if userobj.groups.filter(name='admin').exists() or userobj.groups.filter(name='owner').exists():
                return redirect("home")
            
        else:
            messages.error(request,"Username atau Password salah !!!")
            return redirect("login")
      
        
@login_required(login_url="login")
def performlogout(request):
    logout(request)
    return redirect("login")

@login_required(login_url="login")
@role_required(["owner", 'admin'])
def home(request):
    if not request.user.is_authenticated:
        return render(request, 'logins/login.html')
    else:
        
        # DATA BULANAN
        currentdate = datetime.now()
        tanggalmuda = datetime.now().date().replace(day=1)
        tanggaltua =  currentdate.replace(day=calendar.monthrange(currentdate.year,currentdate.month)[1])

        pemasukanbulan = models.pemesanan.objects.filter(tanggal_pemesanan__range=(tanggalmuda,tanggaltua))
    
        pemesanansebulan = []
        pengirimansebulan = []

        for item in pemasukanbulan:
            getdetailpesan = models.detail_pemesanan.objects.filter(id_pemesanan=item.id_pemesanan)
            for i in getdetailpesan:
                if i.id_pemesanan is not None:
                    totalpemesanan = i.id_pemesanan.id_paket.harga_paket*i.id_pemesanan.jumlah_paket
                    pemesanansebulan.append(totalpemesanan)
                if i.id_pengiriman is not None:
                    totalpengiriman = i.id_pengiriman.id_jenis_pengiriman.tarif_pengiriman
                    pengirimansebulan.append(totalpengiriman)

        totalpemasukanbulanan = sum(pengirimansebulan) + sum(pemesanansebulan)

        # DATA TAHUNAN
        currentdate = datetime.now()
        tahunmulai = datetime.now().date().replace(month=1,day=1)
        tahunakhir = datetime.now().date().replace(month=12,day=31)

        pemasukantahun = models.pemesanan.objects.filter(tanggal_pemesanan__range=(tahunmulai,tahunakhir))
    
        pemesanansetahun = []
        pengirimansetahun = []

        for item in pemasukantahun:
            getdetailpesan = models.detail_pemesanan.objects.filter(id_pemesanan=item.id_pemesanan)
            for i in getdetailpesan:
                if i.id_pemesanan is not None:
                    totalpemesanan = i.id_pemesanan.id_paket.harga_paket*i.id_pemesanan.jumlah_paket
                    pemesanansetahun.append(totalpemesanan)
                if i.id_pengiriman is not None:
                    totalpengiriman = i.id_pengiriman.id_jenis_pengiriman.tarif_pengiriman
                    pengirimansetahun.append(totalpengiriman)

        totalpemasukantahunan = sum(pengirimansetahun) + sum(pemesanansetahun)

        #grafik paket
        pemesananpaket = models.pemesanan.objects.values('id_paket__jenis_paket').annotate(total_pemesanan=Sum('jumlah_paket'))

        
        data1 = []
        for data in pemesananpaket:
           data1.append({
               'paket' : data['id_paket__jenis_paket'],
               'jumlah' : data['total_pemesanan']
           })
        datajson1 = json.dumps(data1)

        # Tabel Paket
        jumlahpemesanan = {}

        for p in pemesananpaket:
            jenis_paket = p['id_paket__jenis_paket']
            total_pemesanan = p['total_pemesanan']
            jumlahpemesanan[jenis_paket] = total_pemesanan

        jumlahpemesanan_couple = jumlahpemesanan.get('Paket Couple',0)
        jumlahpemesanan_ekonomis = jumlahpemesanan.get('Paket Ekonomis',0)
        jumlahpemesanan_healthy = jumlahpemesanan.get('Paket Healthy',0)
        jumlahpemesanan_meatlovers = jumlahpemesanan.get('Paket Meat Lovers',0)
        jumlahpemesanan_allin = jumlahpemesanan.get('Paket All In',0)
        jumlahpemesanan_allinekonomis = jumlahpemesanan.get('Paket All In (Ekonomis)',0)
        jumlahpemesanan_party = jumlahpemesanan.get('Paket Party',0)
        jumlahpemesanan_healing = jumlahpemesanan.get('Paket Healing (Healthy + Suki)',0)

        return render(request,'logins/home.html',{
            'totalpemasukanbulanan' : totalpemasukanbulanan,
            'totalpemasukantahunan' : totalpemasukantahunan,
            'datajson1' : datajson1,
            'jumlahpemesanan_couple' : jumlahpemesanan_couple,
            'jumlahpemesanan_ekonomis' : jumlahpemesanan_ekonomis,
            'jumlahpemesanan_healthy' : jumlahpemesanan_healthy,
            'jumlahpemesanan_meatlovers' : jumlahpemesanan_meatlovers,
            'jumlahpemesanan_allin' : jumlahpemesanan_allin,
            'jumlahpemesanan_allinekonomis' : jumlahpemesanan_allinekonomis,
            'jumlahpemesanan_party' : jumlahpemesanan_party,
            'jumlahpemesanan_healing' : jumlahpemesanan_healing,
        })
    
#ENTITIES

# =====Karyawan===== #

#RKaryawan
@login_required(login_url="login")
@role_required(["owner","admin"])
def karyawan(request):
    karyawanobj = models.karyawan.objects.all()
    return render(request, 'karyawan/karyawan.html',
                  {'karyawanobj': karyawanobj})

#CKaryawan
@login_required(login_url="login")
@role_required(["owner"])
def ckaryawan(request):
    if request.method == 'GET':
        return render(request,'karyawan/ckaryawan.html')
    
    else :
        nama_karyawan_kurir = request.POST['nama_karyawan_kurir']
        no_hp_karyawan_kurir = request.POST['no_hp_karyawan_kurir']

        newkaryawan = models.karyawan(
            nama_karyawan_kurir =  nama_karyawan_kurir,
            no_hp_karyawan_kurir = no_hp_karyawan_kurir,
        )
        newkaryawan.save()
        return redirect('karyawan')

#UKaryawan
@login_required(login_url="login")
@role_required(["owner"])
def ukaryawan(request, id):
    karyawanobj = models.karyawan.objects.get(id_karyawan = id)
    print(karyawanobj)
    if request.method == 'GET':
        return render(request,'karyawan/ukaryawan.html',{
            'karyawanobj':karyawanobj})

    else :
        nama_karyawan_kurir = request.POST['nama_karyawan_kurir']
        no_hp_karyawan_kurir = request.POST['no_hp_karyawan_kurir']

        karyawanobj.nama_karyawan_kurir = nama_karyawan_kurir
        karyawanobj.no_hp_karyawan_kurir = no_hp_karyawan_kurir
        karyawanobj.save()
        return redirect('karyawan')

#DKaryawan
@login_required(login_url="login")
@role_required(["owner"])
def dkaryawan(request, id):
    karyawanobj = models.karyawan.objects.get(id_karyawan = id)
    karyawanobj.delete()

    return redirect('karyawan')


# =====Jenis_pengiriman===== #

#Rjenis_pengiriman
@login_required(login_url="login")
@role_required(["owner","admin"])
def jenis_pengiriman(request):
    jenis_pengirimanobj = models.jenis_pengiriman.objects.all()
    return render(request, 'jenis_pengiriman/jenis_pengiriman.html',
                  {'jenis_pengirimanobj': jenis_pengirimanobj})


#Cjenis_pengiriman
@login_required(login_url="login")
@role_required(["owner"])
def cjenis_pengiriman(request):
        if request.method == 'GET':
            return render(request,'jenis_pengiriman/cjenis_pengiriman.html')
        
        else :
            nama_jenis_pengiriman= request.POST['nama_jenis_pengiriman']
            tarif_pengiriman = request.POST['tarif_pengiriman']

        newjenis_pengiriman = models.jenis_pengiriman(
            nama_jenis_pengiriman =  nama_jenis_pengiriman,
            tarif_pengiriman = tarif_pengiriman,
        )
        newjenis_pengiriman.save()
        return redirect('jenis_pengiriman')


#Ujenis_pengiriman
@login_required(login_url="login")
@role_required(["owner"])
def ujenis_pengiriman(request, id):
    jenis_pengirimanobj = models.jenis_pengiriman.objects.get(id_jenis_pengiriman = id)
    
    if request.method == 'GET':
        return render(request,'jenis_pengiriman/ujenis_pengiriman.html',{
            'jenis_pengirimanobj':jenis_pengirimanobj})
    else :
        nama_jenis_pengiriman= request.POST['nama_jenis_pengiriman']
        tarif_pengiriman = request.POST['tarif_pengiriman']

        jenis_pengirimanobj.nama_jenis_pengiriman = nama_jenis_pengiriman
        jenis_pengirimanobj.tarif_pengiriman = tarif_pengiriman
        jenis_pengirimanobj.save()
        return redirect('jenis_pengiriman')
    

#Djenis_pengiriman
@login_required(login_url="login")
@role_required(["owner"])
def djenis_pengiriman(request, id):
    jenis_pengirimanobj = models.jenis_pengiriman.objects.get(id_jenis_pengiriman = id)
    jenis_pengirimanobj.delete()

    return redirect('jenis_pengiriman')


# =====paket===== #

#Rpaket
@login_required(login_url="login")
@role_required(["owner","admin"])
def paket(request):
    paketobj = models.paket.objects.all()
    return render(request, 'paket/paket.html',
                  {'paketobj': paketobj})


#Cpaket
@login_required(login_url="login")
@role_required(["owner"])
def cpaket(request):
        if request.method == 'GET' :
            return render(request,'paket/cpaket.html')
        
        else :
            jenis_paket = request.POST['jenis_paket']
            harga_paket = request.POST['harga_paket']

            newpaket = models.paket(
                jenis_paket =  jenis_paket,
                harga_paket = harga_paket,
        )
        newpaket.save()
        return redirect('paket')

#Upaket
@login_required(login_url="login")
@role_required(["owner"])
def upaket(request, id):
    paketobj = models.paket.objects.get(id_paket = id)
    
    if request.method == 'GET':
        return render(request,'paket/upaket.html',{
            'paketobj':paketobj})

    else :
        jenis_paket = request.POST['jenis_paket']
        harga_paket = request.POST['harga_paket']

        paketobj.jenis_paket = jenis_paket
        paketobj.harga_paket = harga_paket
        paketobj.save()
        return redirect('paket')


#Dpaket
@login_required(login_url="login")
@role_required(["owner"])
def dpaket(request, id):
    paketobj = models.paket.objects.get(id_paket = id)
    paketobj.delete()

    return redirect('paket')


# =====pelanggan===== #

#Rpelanggan
@login_required(login_url="login")
@role_required(["owner","admin"])
def pelanggan(request):
    pelangganobj = models.pelanggan.objects.all()
    return render(request, 'pelanggan/pelanggan.html',
                  {'pelangganobj': pelangganobj})


#Cpelanggan
@login_required(login_url="login")
@role_required(["admin"])
def cpelanggan(request):
        if request.method == 'GET' :
            return render(request,'pelanggan/cpelanggan.html')
        
        else :
            nama_pelanggan = request.POST['nama_pelanggan']
            alamat = request.POST['alamat']
            no_hp_pelanggan = request.POST['no_hp_pelanggan']

        newpelanggan = models.pelanggan(
            nama_pelanggan =  nama_pelanggan,
            alamat = alamat,
            no_hp_pelanggan  = no_hp_pelanggan ,
        )
        newpelanggan.save()
        return redirect('cpemesanan')


#Upelanggan
@login_required(login_url="login")
@role_required(["admin"])
def upelanggan(request, id):
    pelangganobj = models.pelanggan.objects.get(id_pelanggan = id)
    

    if request.method == 'GET':
        return render(request,'pelanggan/upelanggan.html',{
            'pelangganobj':pelangganobj})
    
    else :
        nama_pelanggan = request.POST['nama_pelanggan']
        alamat = request.POST['alamat']
        no_hp_pelanggan = request.POST['no_hp_pelanggan']

        pelangganobj.nama_pelanggan = nama_pelanggan
        pelangganobj.alamat = alamat
        pelangganobj.no_hp_pelanggan = no_hp_pelanggan
        pelangganobj.save()

    return redirect('pelanggan')

#Dpelanggan
@login_required(login_url="login")
@role_required(["admin"])
def dpelanggan(request, id):
    pelangganobj = models.pelanggan.objects.get(id_pelanggan = id)
    pelangganobj.delete()

    return redirect('pelanggan')


# =====pemesanan===== #

#Rpemesanan
@login_required(login_url="login")
@role_required(["owner","admin"])
def pemesanan(request):
    pemesananobj = models.pemesanan.objects.all()
    tanggal_pemesanan = models.pemesanan.objects.values_list('tanggal_pemesanan')
    tanggal_pengiriman = models.detail_pemesanan.objects.values_list('id_pengiriman__tanggal_pengiriman')
    sekarang = date.today()
    liststatus = []
    for i in range(len(tanggal_pengiriman)):
        tanggal_kembali = tanggal_pengiriman[i][0] + timedelta(days=1)
        print(tanggal_pemesanan[i][0])
        print(tanggal_pengiriman[i][0])
        if sekarang < tanggal_pengiriman [i][0] and tanggal_pemesanan[i][0] <= sekarang :
            status = 'Belum Dikirim'
        else :
            if tanggal_kembali <= sekarang:
                status = 'Sudah Kembali'
            else :
                status = 'Belum Kembali'
        liststatus.append(status)

    i=0
    for item in pemesananobj :
        item.status = liststatus[i]
        i+=1

    return render(request, 'pemesanan/pemesanan.html',
                  {'pemesananobj': pemesananobj})


#Cpemesanan
@login_required(login_url="login")
@role_required(["admin"])
def cpemesanan(request):
        if request.method == 'GET' :
            pelangganobj = models.pelanggan.objects.all()
            paketobj = models.paket.objects.all()
            return render(request,'pemesanan/cpemesanan.html',{
                'datapelanggan' : pelangganobj,
                'datapaket' : paketobj
            })
        
        elif request.method == 'POST':
            id_pelanggan = request.POST["id_pelanggan"]
            id_paket = request.POST["id_paket"]
            jumlah_paket = request.POST['jumlah_paket']
            tanggal_pemesanan = request.POST['tanggal_pemesanan']

            newpemesanan = models.pemesanan.objects.create(
                id_pelanggan_id =  id_pelanggan,
                id_paket_id = id_paket,
                jumlah_paket = jumlah_paket,
                tanggal_pemesanan = tanggal_pemesanan
        )
        newid = newpemesanan.id_pemesanan
        return redirect('cpengiriman', id = newid)


#Upemesanan
@login_required(login_url="login")
@role_required(["admin"])
def upemesanan(request, id):
    pemesananobj = models.pemesanan.objects.get(id_pemesanan = id)
    datapelanggan = models.pelanggan.objects.all()
    datapaket = models.paket.objects.all()

    
    if request.method == 'GET':
        tanggal_pemesanan = datetime.strftime(pemesananobj.tanggal_pemesanan, "%Y-%m-%d")
        return render(request,'pemesanan/upemesanan.html',{
            'pemesananobj': pemesananobj,
            "datapelanggan" : datapelanggan,
            "datapaket" : datapaket,
            'tanggal_pemesanan' : tanggal_pemesanan
            })

    else :
        id_pelanggan = request.POST['id_pelanggan']
        id_paket = request.POST['id_paket']
        pemesananobj.jumlah_paket = request.POST['jumlah_paket']
        pemesananobj.tanggal_pemesanan = request.POST['tanggal_pemesanan']
        getidpelanggan = models.pelanggan.objects.get(id_pelanggan=id_pelanggan)
        getidpaket = models.paket.objects.get(id_paket=id_paket)
        pemesananobj.id_pelanggan = getidpelanggan
        pemesananobj.id_paket = getidpaket
        pemesananobj.save()
        return redirect('pemesanan')


#Dpemesanan
@login_required(login_url="login")
@role_required(["admin"])
def dpemesanan(request, id):
    pemesananobj = models.pemesanan.objects.get(id_pemesanan = id)
    pemesananobj.delete()

    return redirect('pemesanan')


# =====pengiriman===== #


#Rpengiriman
@login_required(login_url="login")
@role_required(["owner","admin"])
def pengiriman(request):
    pengirimanobj = models.pengiriman.objects.all()
    return render(request, 'pengiriman/pengiriman.html',
                  {'pengirimanobj': pengirimanobj})

    
#Cpengiriman
@login_required(login_url="login")
@role_required(["admin"])
def cpengiriman(request, id):
        karyawanobj = models.karyawan.objects.all()
        jenis_pengirimanobj = models.jenis_pengiriman.objects.all()
        if request.method == 'GET' :
            return render(request,'pengiriman/cpengiriman.html',{
                'datakaryawan' : karyawanobj,
                'datajenis_pengiriman' : jenis_pengirimanobj
            })
        
        elif request.method == 'POST' :
            id_karyawan = request.POST['id_karyawan']
            id_jenis_pengiriman = request.POST['id_jenis_pengiriman']
            getid_karyawan =  models.karyawan.objects.get(id_karyawan = id_karyawan)
            getid_jenis_pengiriman = models.jenis_pengiriman.objects.get(id_jenis_pengiriman = id_jenis_pengiriman)
            tanggal_pengiriman = request.POST['tanggal_pengiriman']

            newpengiriman = models.pengiriman.objects.create(
                id_karyawan =  getid_karyawan,
                id_jenis_pengiriman = getid_jenis_pengiriman,
                tanggal_pengiriman = tanggal_pengiriman
                )
            
            models.detail_pemesanan.objects.create(
                id_pemesanan = models.pemesanan.objects.get(id_pemesanan = id),
                id_pengiriman = newpengiriman
            )
        newid = newpengiriman.id_pengiriman
        return redirect('detail_pemesanan')


#Upengiriman
@login_required(login_url="login")
@role_required(["admin"])
def upengiriman(request, id):
    pengirimanobj = models.pengiriman.objects.get(id_pengiriman = id)
    datakaryawan = models.karyawan.objects.all()
    datajenis_pengiriman = models.jenis_pengiriman.objects.all()

    
    if request.method == 'GET':
        tanggal_pengiriman = datetime.strftime(pengirimanobj.tanggal_pengiriman, "%Y-%m-%d")
        return render(request,'pengiriman/upengiriman.html',{
            'pengirimanobj': pengirimanobj,
            "datakaryawan" : datakaryawan,
            "datajenis_pengiriman" : datajenis_pengiriman,
            'tanggal_pengiriman': tanggal_pengiriman
            })

    else :
        id_karyawan = request.POST['id_karyawan']
        id_jenis_pengiriman = request.POST['id_jenis_pengiriman']
        pengirimanobj.tanggal_pengiriman = request.POST['tanggal_pengiriman']
        getidkaryawan = models.karyawan.objects.get(id_karyawan=id_karyawan)
        getidjenis_pengiriman = models.jenis_pengiriman.objects.get(id_jenis_pengiriman=id_jenis_pengiriman)
        pengirimanobj.id_karyawan = getidkaryawan
        pengirimanobj.id_jenis_pengiriman = getidjenis_pengiriman
        pengirimanobj.save()
        return redirect('pengiriman')
    

#Dpengiriman
@login_required(login_url="login")
@role_required(["admin"])
def dpengiriman(request, id):
    pengirimanobj = models.pengiriman.objects.get(id_pengiriman = id)
    pengirimanobj.delete()

    return redirect('pengiriman')


# =====detail_pemesanan===== #


#Rdetail_pemesanan
@login_required(login_url="login")
@role_required(["owner","admin"])
def detail_pemesanan(request):
    detail_pemesananobj = models.detail_pemesanan.objects.all()
    return render(request, 'detail_pemesanan/detail_pemesanan.html',
                  {'detail_pemesananobj': detail_pemesananobj})

    
#Cdetail_pemesanan
@login_required(login_url="login")
@role_required(["admin"])
def cdetail_pemesanan(request):
        if request.method == 'GET' :
            pemesananobj = models.pemesanan.objects.all()
            pengirimanobj = models.pengiriman.objects.all()
            return render(request,'detail_pemesanan/cdetail_pemesanan.html',{
                'datapemesanan' : pemesananobj,
                'datapengiriman' : pengirimanobj
            })
        
        elif request.method == 'POST':
            id_pemesanan = request.POST["id_pemesanan"]
            id_pengiriman = request.POST["id_pengiriman"]
            getid_pemesanan = models.pemesanan.objects.get(id_pemesanan = id_pemesanan)
            getid_pengiriman = models.pengiriman.objects.get(id_pengiriman = id_pengiriman)

            newdetail_pemesanan = models.detail_pemesanan.objects.create(
                id_pemesanan_id =  getid_pemesanan,
                id_pengiriman_id = getid_pengiriman,
        )
        newdetail_pemesanan.save()
        return redirect('detail_pemesanan')
    

#Ddetail_pemesanan
@login_required(login_url="login")
@role_required(["admin"])
def ddetail_pemesanan(request, id):
    detail_pemesananobj = models.detail_pemesanan.objects.get(id_detail_pemesanan = id)
    detail_pemesananobj.delete()

    return redirect('detail_pemesanan')

# LAPORAN 
@login_required(login_url="login")
@role_required(["owner", 'admin'])
def laporanpemesanan(request):
    if request.method == "GET":
        return render(request, 'laporan/createlaporan_pemesanan.html')
    
    elif request.method == "POST":
        laporanobj = []
        listtotalpemesanan = []
        print(laporanobj)

        mulai = request.POST['mulai']
        akhir = request.POST['akhir']
        filterpemesanan = models.pemesanan.objects.filter(tanggal_pemesanan__range=(mulai, akhir))

        for item in filterpemesanan:
            datadetailpemesanan = []
            getdetailpemesanan = models.detail_pemesanan.objects.filter(id_pemesanan_id = item.id_pemesanan)
            datadetailpemesanan.append(item)
            datadetailpemesanan.append(getdetailpemesanan)
            listtotal = []

            for i in getdetailpemesanan :
                    totalpemesanan = (i.id_pemesanan.id_paket.harga_paket*i.id_pemesanan.jumlah_paket) + i.id_pengiriman.id_jenis_pengiriman.tarif_pengiriman
                    listtotal.append(totalpemesanan)

            datadetailpemesanan.append(listtotal)
            grandtotal = sum(listtotal)
            listtotalpemesanan.append(grandtotal)
            datadetailpemesanan.append(grandtotal)
            laporanobj.append(datadetailpemesanan)
        totalkeseluruhan = sum(listtotalpemesanan)

    return  render(request, 'laporan/laporan_pemesanan.html', {
            'laporanobj' : laporanobj,
            'totalkeseluruhan' : totalkeseluruhan,
            'mulai': mulai,
            'akhir': akhir,
            })        

@login_required(login_url="login")
@role_required(["owner", 'admin'])
def laporanpdf(request,mulai,akhir):
    laporanobj = []
    listtotalpemesanan = []
    filterpemesanan = models.pemesanan.objects.filter(tanggal_pemesanan__range=(mulai, akhir))

    for item in filterpemesanan:
        datadetailpemesanan = []
        getdetailpemesanan = models.detail_pemesanan.objects.filter(id_pemesanan_id = item.id_pemesanan)
        datadetailpemesanan.append(item)
        datadetailpemesanan.append(getdetailpemesanan)
        listtotal = []

        for i in getdetailpemesanan :
                totalpemesanan = (i.id_pemesanan.id_paket.harga_paket*i.id_pemesanan.jumlah_paket) + i.id_pengiriman.id_jenis_pengiriman.tarif_pengiriman
                listtotal.append(totalpemesanan)

        datadetailpemesanan.append(listtotal)
        grandtotal = sum(listtotal)
        listtotalpemesanan.append(grandtotal)
        datadetailpemesanan.append(grandtotal)
        laporanobj.append(datadetailpemesanan)
    totalkeseluruhan = sum(listtotalpemesanan)

    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=laporan.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    html_string = render_to_string(
        'laporan/laporanpdf.html',{
            'laporanobj' : laporanobj,
            'totalkeseluruhan' : totalkeseluruhan,
            'mulai': mulai,
            'akhir': akhir,
            })
    html = HTML(string=html_string)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())
    
    render(request, 'laporan/laporanpdf.html')

    return response
    