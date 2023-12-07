from werkzeug.security import generate_password_hash
import csv
from faker import Faker

num_users = 100
num_products = 2000
num_purchases = 2500

Faker.seed(0)
fake = Faker()

images = [
          "https://m.media-amazon.com/images/I/61eMsTk4w0L._SX385_.jpg",
          "https://m.media-amazon.com/images/I/61Qf8Ztg1FL._SX425_.jpg",
          "https://m.media-amazon.com/images/I/81WQdDu1A6L._SX522_.jpg",
          "https://images-na.ssl-images-amazon.com/images/I/41sQ-wEF2ML._AC_UL675_SR675,480_.jpg",
          "https://images-na.ssl-images-amazon.com/images/I/518cRYanpbL._AC_UL675_SR675,480_.jpg",
          "https://images-na.ssl-images-amazon.com/images/I/61j4Q05bJuL._AC_UL675_SR675,480_.jpg"
          ]

def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            writer.writerow([uid, email, password, firstname, lastname])
        print(f'{num_users} generated')
    return


def gen_bids(num_products):
    n_users = 0 
    available_pids = []
    with open('Bids.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Bids...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
                print(f'{n_users}', end=' ', flush=True)
                n_users += 1
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            writer.writerow([pid, 0, pid, price])
        print(f'{num_products} generated;')
    return available_pids


def gen_products(num_products):
    available_pids = []
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            description = fake.sentence(nb_words=20)
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            buynow = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            available = fake.random_element(elements=('true', 'false'))
            catergory = fake.random_element(elements=('food&drink', 'art&decor', 'electronics'))
            image = fake.random_element(elements=(images))
            expirytime = fake.future_datetime(end_date='+365d')
            rating = f'{str(fake.random_int(min=1, max=4))}.{fake.random_int(min=0, max=99):02}'
            if available == 'true':
                available_pids.append(pid)
            writer.writerow([pid, name, price, buynow, available, catergory, expirytime, image, rating, description])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids


# def gen_amazon_products(num_products):
#     available_pids = []
#     with open('Productstest.csv', 'w') as f:
#         writer = get_csv_writer(f)
#         print('Products...', end=' ', flush=True)
#         m = scrapeproducts.scrape(num_products)
#         for pid in range(num_products):
#             if pid % 100 == 0:
#                 print(f'{pid}', end=' ', flush=True)
#             name = m[pid][0]
#             price = m[pid][1]
#             available = fake.random_element(elements=('true', 'false'))
#             rating = m[pid][2]
#             if available == 'true':
#                 available_pids.append(pid)
#             writer.writerow([int(pid), name, price, available])
#         print(f'{num_products} generated; {len(available_pids)} available')
#     return available_pids


def gen_purchases(num_purchases, available_pids):
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            time_purchased = fake.date_time()
            writer.writerow([id, uid, pid, time_purchased])
        print(f'{num_purchases} generated')
    return


gen_users(num_users)
available_pids = gen_products(num_products)
gen_purchases(num_purchases, available_pids)
gen_bids(num_products)

