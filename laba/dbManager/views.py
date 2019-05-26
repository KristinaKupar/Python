from django.shortcuts import render, HttpResponseRedirect
from .database_handler import DataBase
import time
from .forms import PartFrom
# Create your views here.

my_db = DataBase()


def show_songs(request):
    table = my_db.get_songs()
    return render(request, 'dmManager/songs.html', {'response': {"songs": table}})
    #return render(request, 'dmManager/songs.html', {'response': {"songs": table}})


def show_singers_in_range(request):
    if request.POST["Min"] != "" and request.POST["Max"] != "":
        table = my_db.get_singers_in_range(request.POST)
    else:
        table = my_db.get_singers()
    return render(request, 'dmManager/singers.html', {'response': {'singers': table}})


def show_singers(request):
    table = my_db.get_singers()
    return render(request, 'dmManager/singers.html', {'response': {'singers': table}})


def show_history(request):
    table = my_db.get_history()
    return render(request, 'dmManager/history.html', {'response': {'history': table}})


def delete_order(request):
    if request.method == "POST":
        if request.POST.get("DeleteOrder", False) != "":
            my_db.delete_order_by_id(request)
    return HttpResponseRedirect('/history')


def add_order(request):
    if request.method == "POST":
        if request.POST["Cust_name"] != "" and request.POST["Song_name"] != "":
            customers = my_db.get_customer(request)
            song = my_db.get_song_by_name(request.POST["Song_name"])
            date = time.strftime("%y/%m/%d")
            if customers:
                for a in customers:
                    idCust = str(a)
            if song:
                for s in song:
                    idSong = str(s)
            if customers and song:
                my_db.insert_order(idCust, idSong, date)
    return HttpResponseRedirect('/history')


def edit_order(request):
    if request.method == "POST":
        #if request.POST["Cust_id_edit"] != ""\
         #       and request.POST["Cust_song_edit"] != "":
          #  song = my_db.get_song_by_name(request.POST["Cust_song_edit"])
           # if song:
            #    print str(song[0])
             #   my_db.update_order(str(song[0]), request.POST["Cust_id_edit"])
        name = PartFrom(request.POST)
        if name.is_valid():
            return HttpResponseRedirect('/history')

    else:
        name = PartFrom(('list', "notlost"))
    return render(request, 'dmManager/history.html', {"names", name})


def find(request):
    if request.method == "POST":
        if request.POST["text"] != "":
            table = my_db.find_in_boolean_mode(request.POST["text"])
        else:
            table = my_db.get_songs()
        print table
        return render(request, 'dmManager/songs.html', {'response': {"songs": table}})


def insert(request):
    if request.method == "POST":
        if request.POST["name"] != "" and request.POST["style"] != "" \
                and request.POST["singer_name"] != "" and request.POST["len"] != "":
            table = my_db.get_id_by_name(request.POST["singer_name"])
            if table:
                for a in table:
                    id1 = str(a)
                my_db.insert_song(request.POST, id1)
        return HttpResponseRedirect('/')


def edit_songs(request):
    if request.method == "POST":
        if request.POST["idEdit"] != "" and request.POST["nameEdit"] != "" and request.POST["styleEdit"] != "" \
                and request.POST["singer_nameEdit"] != "" and request.POST["lenEdit"] != "":
            table = my_db.get_id_by_name(request.POST["singer_nameEdit"])
            if table:
                for a in table:
                    id = str(a)
            my_db.update_song(request.POST, id)
        return HttpResponseRedirect('/')


def delete_singers(request):
    if request.method == "POST":
        if request.POST["idDelete"] != "":
            my_db.delete_songs_by_id(request.POST["idDelete"])
            my_db.delete_singer_by_id(request.POST["idDelete"])
    return HttpResponseRedirect('/')


def load_from_file(request):
    if request.method == "POST":
        my_db.parse_xml()
        return HttpResponseRedirect('/')
