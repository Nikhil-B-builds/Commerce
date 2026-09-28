# Commerce

A Django-based e-commerce auction platform inspired by online auction marketplaces. Users can create listings, place bids, add items to their wishlist, comment on listings, browse by category, and close auctions.

This project was built as part of **CS50's Web Programming with Python and JavaScript (CS50W)** and was my first major project involving a relational database and Django's ORM.

## Features

### 👤 User Authentication

* User registration and login
* Logout functionality
* Django authentication system
* User-specific actions and permissions

### 🏷️ Listings

* Create auction listings
* Add:

  * Listing name
  * Description
  * Starting/current price
  * Category
  * Image
* View individual listing pages
* Browse active listings

### 💰 Bidding

* Users can place bids on active listings
* Bids must be higher than the current price
* The highest bidder is tracked
* Previous bids are stored in the database

### ⭐ Wishlist

* Add listings to a personal wishlist
* Remove listings from the wishlist
* View wishlist items separately

### 💬 Comments

* Users can comment on listings
* Existing comments are displayed on the listing page

### 🔨 Auction Closing

* Listing owners can close their auctions
* The highest bidder becomes the winner
* Closed listings are marked as sold

### 📂 Categories

* Listings can be assigned to categories
* Browse listings based on category

### 🛠️ Admin Interface

* Django admin is configured for managing application data

---

## Tech Stack

* **Python**
* **Django**
* **SQLite**
* **HTML**
* **CSS**
* **Django Templates**
* **Django ORM**
* **Git & GitHub**

---

## Project Structure

```text
Commerce/
│
├── auctions/
│   ├── migrations/
│   ├── templates/
│   │   └── auctions/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── commerce/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## Database Models

The application uses Django's ORM to manage its relational database.

The main entities include:

* **User** — registered users of the application
* **Listing** — auction items created by users
* **Bid** — bids placed on listings
* **Comment** — comments made on listings
* **Wishlist** — listings saved by users
* **Sold** — information about closed/sold auctions
* **Createdby** — associates listings with their creators

These models are connected using Django relationships such as `ForeignKey` and `OneToOneField`.

---

## How It Works

A simplified flow for creating and interacting with a listing:

```text
User
 │
 ├── Creates Listing
 │       │
 │       ├── Category
 │       ├── Bids
 │       ├── Comments
 │       └── Wishlist
 │
 └── Places Bid
         │
         └── Listing price updates
                 │
                 └── Auction closes
                         │
                         └── Highest bidder wins
```

Django's ORM handles communication between the application and the database, allowing database operations to be performed through Python instead of writing raw SQL for every operation.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Nikhil-B-builds/Commerce.git
cd Commerce
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create an admin account

```bash
python manage.py createsuperuser
```

Follow the prompts to create the administrator account.

### 6. Start the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## Main Routes

| Route         | Purpose                   |
| ------------- | ------------------------- |
| `/`           | View active listings      |
| `/login`      | Log in                    |
| `/register`   | Create an account         |
| `/create`     | Create a new listing      |
| `/categories` | Browse listing categories |
| `/wishlist`   | View saved listings       |
| `/admin`      | Django administration     |

---

## What I Learned

This project was my first major experience building an application around a relational database.

Some of the main concepts I worked with were:

* Django models
* Database migrations
* Django ORM
* Foreign-key relationships
* One-to-one relationships
* CRUD operations
* Authentication
* Sessions
* Forms and validation
* URL routing
* Template inheritance
* POST requests
* CSRF protection
* Managing persistent application state

One of the biggest lessons from the project was that working with a database is not only about knowing SQL syntax. The more difficult part is designing the data relationships and deciding how application state should be represented and updated.

---

## Future Improvements

Possible improvements include:

* Improve the overall UI and responsive design
* Add automated tests
* Improve error handling
* Add pagination for listings
* Add search functionality
* Improve database query efficiency
* Refactor views into smaller components
* Add stronger validation for auction and bidding logic
* Improve deployment configuration

---

## Project Status

**Completed — CS50W Commerce Project**

The core functionality of the application is complete. Further improvements would primarily focus on UI polish, testing, code organization, security, and production deployment.

---

## Author

**Nikhil**

GitHub:
https://github.com/Nikhil-B-builds
