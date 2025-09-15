# object-detection-and-tracking

# Database
Berikut adalah design dari database yang saya buat, disini terdapat 3 buah table, dua diantara memiliki relasi ke dalam table polygon

![alt text](https://github.com/Venator43/object-detection-and-tracking/blob/main/Diagram/sh-Page-1.drawio.png)

Untuk database yang saya gunakan sendiri, saya menggunakan MySQL dan saya sudah menyediakan file sql bernama "hd.sql" yang dapat langsung anda import untuk dapat menjalankan aplikasi saya

# Datasets
Terdapat 2 buah dataset yang saya gunakan pada aplikasi ini, untuk melakukan testing algoritma, saya menggunakan video static yang saya dapatkan dari : https://www.youtube.com/watch?v=ORrrKXGx2SE&pp=ygUgd2Fsa2luZyBwZW9wbGUgYmFja2dyb3VuZCB2aWRlbyA%3D
Untuk aplikasi utamanya sendiri, saya menggunakan video live stream yang saya daptkan dari webiste CCTV public kota bandung, website tersebut dapat dikunjungi melalui link berikut : https://pelindung.bandung.go.id/ 

# Object Detection & Tracking
Design system object detection yang saya kembangkan adalah sebagai berikut
![alt text](https://github.com/Venator43/object-detection-and-tracking/blob/main/Diagram/hs.drawio.png)

# Deployment
sebelum anda menjalankan program saya, pertama anda harus mengimport database yang telah saya buat, kemudian, anda harus menambahkan configurasi dabase anda ke dalam file "config.yaml"

Saya menyediakan 2 cara untuk menjalnkan program yang saya buat, satu melalui docker, dan satu tanpa menggunakan docker
untuk menjalankan program yang telah saya buat menggunakan docker, anda dapat dengan mudah menggunakan command "docker-compose up" untuk mem-build dan menjalankan program didalam docker, kemudian, anda dapat mengakses video object detection dengan memasuki URL : "http://localhost:5000/" dan untuk mengakses API dapat masuk URL : "http://localhost:8000/docs"

Jika anda tidak menggunakan docker, pertama anda harus menginstall package yang dibutuhkan dengan menggunakan command "pip install -r requirements.txt" kemudian anda dapat menjalankan program API dengan cara menggunakan command "python api.py" dan menjalankan program object detection dengan menggunakan command "python main.py" setelah emnjalankan kedua program tersebut, sama seperti pada docker anda dapat mengakses API dengan cara memasuki URL : "http://localhost:8000/docs" dan video object detection dengan cara memasuki URL : "http://localhost:5000/"

Selain menggunakan website untuk menjalankan program object detection dan tracking, anda juga dapat menjalankan versi non-web program dengan menjalankan command "python live.py" untuk menjalankan program menggunakan video livestream atau "python static.py" untuk menjalankan program menggunakan video static
