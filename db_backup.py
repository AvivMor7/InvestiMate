from cities import *
from datetime import datetime

def dump_db_to_txt():
    cities = load_cities_from_db()
    try:
        with open('cities_dump.txt', 'w', encoding='utf-8') as file:
            # Write the current date as the first line
            dump_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"DUMP DATE: {dump_date}\n\n")

            # Write each city's data to the file
            for city in cities:
                file.write(f"id: {city.id}\n")
                file.write(f"eng_name: {city.eng_name}\n")
                file.write(f"heb_name: {city.heb_name}\n")
                file.write(f"avg_rent: {city.avg_rent}\n")
                file.write(f"avg_sell: {city.avg_sell}\n\n")

        print("Data dumped to cities_dump.txt successfully.")

    except Exception as e:
        print(f"Error dumping data to file: {e}")
        
def save_to_db_from_txt():
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
            # Read data from the text file, skipping the first line
            with open('cities_dump.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()[1:]  # Skip the first line

                # Process each city block (assuming each city data is separated by an empty line)
                city_data = []
                for line in lines:
                    line = line.strip()
                    if line:
                        city_data.append(line)
                    else:
                        if city_data:
                            # Process the collected data for each city
                            city = City(
                                id=int(city_data[0].split(': ')[1]),
                                eng_name=city_data[1].split(': ')[1],
                                heb_name=city_data[2].split(': ')[1],
                                avg_rent=float(city_data[3].split(': ')[1]),
                                avg_sell=float(city_data[4].split(': ')[1])
                            )
                            # Insert or update city data in the database
                            sql = """
                                REPLACE INTO cities (id, eng_name, heb_name, avg_rent, avg_sell)
                                VALUES (%s, %s, %s, %s, %s)
                            """
                            cursor.execute(sql, (city.id, city.eng_name, city.heb_name, city.avg_rent, city.avg_sell))
                            conn.commit()
                            
                            # Reset city_data for the next city
                            city_data = []

                # Process the last city if any
                if city_data:
                    city = City(
                        id=int(city_data[0].split(': ')[1]),
                        eng_name=city_data[1].split(': ')[1],
                        heb_name=city_data[2].split(': ')[1],
                        avg_rent=float(city_data[3].split(': ')[1]),
                        avg_sell=float(city_data[4].split(': ')[1])
                    )
                    # Insert or update city data in the database
                    sql = """
                        REPLACE INTO cities (id, eng_name, heb_name, avg_rent, avg_sell)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (city.id, city.eng_name, city.heb_name, city.avg_rent, city.avg_sell))
                    conn.commit()

        print("Data saved from cities_dump.txt to database successfully.")

    except Exception as e:
        print(f"Error saving data to database: {e}")

    finally:
        # Close connection
        conn.close()
