from typing import Tuple, List
import json
from dataclasses import dataclass, field, asdict
import csv

@dataclass
class Category:
    id: int
    name: str

@dataclass
class Product:
    id: int
    asin: str
    discontinued: bool
    group_name: str | None = field(default=None)
    title: str | None = field(default=None)
    categories: List[int] | None = field(default=None)
    salesrank: int | None = field(default=None)
    similars_count: int | None = field(default=None)
    avg_rating: float | None = field(default=None)
    total_reviews: int | None = field(default=None)
    downloaded_reviews: int | None = field(default=None)

@dataclass
class Similar:
    asin: str
    similar_asin: str

@dataclass
class Review:
    product_id: int
    customer_id: str
    time: str
    rating: int
    votes: int
    helpful: int

categories = []
products = []
reviews = []
similars = []

def title_parse(line: str) -> Tuple[str, str]:
    # key = line[2:7]
    value = line[9:]
    return value

def parse(line: str) -> str:
    key, value = line.replace(' ', '').split(':')
    return value

def similar_parse(line: str):
    parts = line.split('  ')
    count = int(parse(parts[1]))
    return count, parts[2:]

def categories_parse(lines: List[str]) -> List[List[str]]:
    global categories

    categories_int = []
    for line in lines:
        categories_str = line.replace('   |', '').split('|')
        for category in categories_str:
            parts = category.split('[')
            len_parts = len(parts)
            category = ''
            for i in range(len_parts - 1):
                category += parts[i]

            # category = parts[0]
            category_id = int(parts[len_parts - 1].replace(']', ''))
            category = Category(id=category_id, name=category)
            if not category in categories:
                categories.append(category)
            categories_int.append(category_id)
            

    return set(categories_int)

def reviews_parse(product_id, lines: List[str]):
    global reviews

    parts = lines[0].replace('  reviews: ', '').split('  ')
    total = int(parse(parts[0]))
    downloaded = int(parse(parts[1]))
    avg_rating = float(parse(parts[2]))

    for line in lines[1:]:
        review = line.replace(':     ', ': ').replace(':   ', ': ').replace(':  ', ': ').split('  ')
        time = review[2]
        customer = parse(review[3])
        rating = int(parse(review[4]))
        votes = int(parse(review[5]))
        helpful = int(parse(review[6]))

        reviews.append(Review(
            product_id=product_id,
            customer_id=customer,
            time=time,
            rating=rating,
            votes=votes,
            helpful=helpful
        ))

    return {
        'total': total,
        'downloaded': downloaded,
        'avg_rating': avg_rating
    }


def parse_item(item: str) -> dict[str, str]:
    global products
    global similars

    lines = item.split('\n')

    product_id = int(parse(lines[0]))
    asin = parse(lines[1])
    product = Product(id=product_id, asin=asin, discontinued=True)

    if len(lines) >= 6:
        product_title = title_parse(lines[2])
        group_name = parse(lines[3]) 

        product_salesrank = int(parse(lines[4]))
        similars_count, product_similars = similar_parse(lines[5])

        for similar in product_similars:
            pair = Similar(asin=asin, similar_asin=similar)
            pair2 = Similar(asin=similar, similar_asin=asin)
            if not pair in similars and not pair2 in similars:
                similars.append(pair)

        
        categories_count = int(parse(lines[6]))
        categories = list(categories_parse(lines[7:7 + categories_count]))
        reviews_dict = reviews_parse(product_id, lines[7 + categories_count:])
        avg_rating = reviews_dict['avg_rating']
        total_reviews = reviews_dict['total']
        downloaded_reviews = reviews_dict['downloaded']

        product = Product(
            id=product_id,
            asin=asin,
            discontinued=False,
            group_name=group_name,
            title=product_title,
            categories=categories,
            salesrank=product_salesrank,
            similars_count=similars_count,
            avg_rating=avg_rating,
            total_reviews=total_reviews,
            downloaded_reviews=downloaded_reviews
        )

    products.append(product)

# with open('./data/categories.csv', 'r', encoding='utf-8', newline='') as file:
#     reader = csv.DictReader(file)
#     for row in reader: 
#         categories.append(Category(id=int(row['id']), name=row['name']))



with open('C:\\Users\\vladi\\Documents\\yandex\\product_graph\\metadata.txt', 'r', encoding='utf-8') as file:
    total = file.readline()
    file.readline()
    items = file.read().split('\n\n')

    count = 0

    for item in items:
        count += 1

        if count <= 545000:
            continue 

        try:
            item_dict = parse_item(item) 
        except ValueError as e:
            print(e)
            print(count)
            break

        if count % 1000 == 0:
            print(count // 1000, 'из 548') 

with open('./data/categories.csv', 'a', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, ['id', 'name'])
    # writer.writeheader()
    for category in categories:
        writer.writerow(asdict(category))

with open('./data/products.tsv', 'a', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, [
        'id', 
        'asin', 
        'discontinued', 
        'group_name', 
        'title', 
        'categories', 
        'salesrank', 
        'similars_count', 
        'avg_rating', 
        'total_reviews', 
        'downloaded_reviews'], delimiter='\t')
    
    # writer.writeheader()
    for product in products:
        writer.writerow(asdict(product))

with open('./data/similar.csv', 'a', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, ['asin', 'similar_asin'])
    
    # writer.writeheader()
    for similar in similars:
        writer.writerow(asdict(similar))

with open('./data/reviews.csv', 'a', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, [
        'product_id',
        'customer_id',
        'time',
        'rating',
        'votes',
        'helpful'])
    
    # writer.writeheader()
    for review in reviews:
        writer.writerow(asdict(review))