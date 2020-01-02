import mysql.connector

# Connect DB
db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password"
)

if db.is_connected():
    try:
        print("Berhasil terhubung ke database")

        cursor = db.cursor()
        cursor.execute("CREATE DATABASE naive")

        print("Database berhasil dibuat!")

        # Select DB
        cursor.execute("USE naive")

        # Create Table
        # Table Category
        kategori = """
                CREATE TABLE `kategori` (
                  `id` int(11) NOT NULL AUTO_INCREMENT,
                  `nama_kategori` varchar(45) NOT NULL,
                  PRIMARY KEY (`id`)
                )
            """
        cursor.execute(kategori)

        print("Tabel kategori berhasil dibuat!")

        # Table Comment
        komentar = """
                  CREATE TABLE `komentar` (
                      `id` int(11) NOT NULL AUTO_INCREMENT,
                      `komentar` varchar(45) NOT NULL,
                      `kategori_id` int(11) DEFAULT NULL,
                      PRIMARY KEY (`id`)
                    )
                """
        cursor.execute(komentar)

        print("Tabel komentar berhasil dibuat!")
    except Exception as e:
        print("Error pembuatan database", e)