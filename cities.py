import pymysql

class City:
    def __init__(self, id=None, eng_name=None, heb_name=None, avg_rent=None, avg_sell=None):
        self.id = id
        self.eng_name = eng_name
        self.heb_name = heb_name
        self.avg_rent = avg_rent
        self.avg_sell = avg_sell

    def __repr__(self):
        return (f"City(ID: {self.id}, English Name: {self.eng_name}, "
                f"Hebrew Name: {self.heb_name}, "
                f"Avg Rent: {self.avg_rent}, "
                f"Avg Selling Price: {self.avg_sell})")

def load_cities_from_db(city_name=None):
    cities = []
    # Connect to MySQL
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='##########',
        database='Mashcanta_DB',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with conn.cursor() as cursor:
            if city_name:
                # Select query to retrieve a specific city by its hebrew name
                sql = "SELECT * FROM cities WHERE heb_name REGEXP %s"
                cursor.execute(sql, (city_name,))
                result = cursor.fetchone()

                if result:
                    city = City(
                        id=result['id'],
                        eng_name=result['eng_name'],
                        heb_name=result['heb_name'],
                        avg_rent=result['avg_rent'],
                        avg_sell=result['avg_sell']
                    )
                    print("City loaded successfully.")
                    return city
            else:
                # Select query to retrieve all cities data
                sql = "SELECT * FROM cities"
                cursor.execute(sql)
                results = cursor.fetchall()

                # Iterate over results and create City objects
                for result in results:
                    city = City(
                        id=result['id'],
                        eng_name=result['eng_name'],
                        heb_name=result['heb_name'],
                        avg_rent=result['avg_rent'],
                        avg_sell=result['avg_sell']
                    )
                    cities.append(city)

        print("Cities loaded successfully.")
        return cities

    except Exception as e:
        print(f"Error loading cities: {e}")
        return []

    finally:
        # Close connection
        conn.close()


def save_cities_to_db(city):
    # Connect to MySQL
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='55555aviv',
        database='Mashcanta_DB',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with conn.cursor() as cursor:
            if isinstance(city, list):
                # Handle list of cities
                for c in city:
                    if c.id is None:
                        # Insert new city
                        sql = "INSERT INTO cities (eng_name, heb_name, avg_rent, avg_sell) VALUES (%s, %s, %s, %s)"
                        cursor.execute(sql, (c.eng_name, c.heb_name, c.avg_rent, c.avg_sell))
                        conn.commit()
                        c.id = cursor.lastrowid  # Update the city object with the generated id
                        print(f"City '{c.eng_name}' inserted successfully with id {c.id}")
                    else:
                        # Update existing city
                        sql = "UPDATE cities SET eng_name=%s, heb_name=%s, avg_rent=%s, avg_sell=%s WHERE id=%s"
                        cursor.execute(sql, (c.eng_name, c.heb_name, c.avg_rent, c.avg_sell, c.id))
                        conn.commit()
                        print(f"City '{c.eng_name}' updated successfully")
            else:
                # Handle single city
                if city.id is None:
                    # Insert new city
                    sql = "INSERT INTO cities (eng_name, heb_name, avg_rent, avg_sell) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (city.eng_name, city.heb_name, city.avg_rent, city.avg_sell))
                    conn.commit()
                    city.id = cursor.lastrowid  # Update the city object with the generated id
                    print(f"City '{city.eng_name}' inserted successfully with id {city.id}")
                else:
                    # Update existing city
                    sql = "UPDATE cities SET eng_name=%s, heb_name=%s, avg_rent=%s, avg_sell=%s WHERE id=%s"
                    cursor.execute(sql, (city.eng_name, city.heb_name, city.avg_rent, city.avg_sell, city.id))
                    conn.commit()
                    print(f"City '{city.eng_name}' updated successfully")
    except Exception as e:
        print(f"Error saving city: {e}")

    finally:
        # Close connection
        conn.close()
