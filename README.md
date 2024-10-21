# Introduction

This Repo contains the Practical work on GraphQL and gRPC

## Installation

### 1. With a docker container

If docker is installed on your computer, you must :

1. clone the github repository
2. open a cmd
3. go into the repository using

   ```bash
   cd path/to/your/repository
   ```

4. open the docker app to start the kernel
5. run

   ```
   docker-compose up --build
   ```

### 2. Without a docker container

If you don't have docker on your computer, you can :

1. clone the github repository
2. open a 4 cmd
3. go into the repository using

   ```bash
   cd path/to/your/repository
   ```

4. go into showtimes using

   ```bash
   cd ./showtime
   ```

5. then, to launch the service, use

   ```bash
   python showtime.py
   ```

6. repeat in a different cmd for user, movie and booking

## What we did

We suceeded to finish the integrality of what was asked in this pratical work. This Pratical Work translate the TP REST in graphql and in gRPC. With graphql, we can choose during the request the elements which will be returned so several methods can be converted into one graphql schema. Let's see what we add in each service :

### Movies

As explained before we suceeded to produce a service movie which respects what was ask in the practical work.
Then, it is a graphql service with 2 entries : _"/"_ and _"/graphql"_ which is a **POST** entry. The entry point _"/"_ returns the homepage of the service (an **html** page). The entry point _"graphql"_ allows us to use a **graphql schema** to ask the elements needed. The schema are written in _./movie.graphql_ and the resolvers in _./movie/resolvers.py_.

### Bookings

Booking is a gRPC service which can call **Showtimes**. This folder contains two _.proto_ files : _booking.proto_ which is copied into the _user_ folder and _showtime.proto_ which is the same that the _.proto_ file in the folder _showtime_.

Let's see each methods of Booking :

- _GetAllBookings_ returns all the bookings which were made

- _GetBookingForUser_ returns the booking made by the user given

- _AddBookingByUser_ adds a booking to the user given. The parameters of the booking are given by the entry message

- _GetMovieAtDate_ returns the movies available at the date given

### User

User is at the same time a gRPC client and an REST API using graphql server. Indeed, **User** calls **Booking** in _./user/resolvers.py_. It has only one entry point : _"/graphql"_.
