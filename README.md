# Semantic Image Search with Redis

This demo show how implement a semantic image search using the entire contents of the [National Gallery of Art](https://www.nga.gov/). It has all the code needed to load the images, create embeddings from them, and store them in Redis as well as to then use these embeddings to search for similar images.

This README instructs you on how to get this demo up and running.


## Requirements

You'll need the following bits and bobs installed to get this demo up and running:

- A recent version of Docker—to run Redis 8
- Python 3.12, and _not_ Python 3.13—to run the art-deco-server and, very optionally, the art-deco-loader.
- A recent version of Node.js, I used Node.js v22.15—to run the art-deco-client

Downloading and installing these fine things is left as an exercise for the end user.


## Running the demo

You will need to [install Redis](#install-and-run-redis), [start the art-deco-server](#run-the-server), start the [art-deco-client](#run-the-client), and optionally run the [art-deco-loader](#run-the-loader-not-recommended).


### Install and run Redis

First things first, we need some Redis. I have conveniently provided a [docker-compose.yaml](redis/docker-compose.yaml) file in the [redis](redis) folder to do this for you. Note that there is a rather large file named [dump.rdb](redis/dump.rdb) in this folder as well. It contains the results of the [art-deco-loader](art-deco-loader) having been run and will be loaded by Redis automatically.


```bash
cd redis
docker compose up
```


### Run the server

Next we need the server running. In a _new terminal_, set up the server's Python environment:

```bash
cd art-deco-server
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Once it is set up you can run it with:

```bash
fastapi dev main.py
```

You can see if it is running by hitting the root server at http://localhost:8000 with your browser. You should get back:

```json
{
  "status": "OK"
}
```


### Run the client

To run the client, you'll need to set up your Node.js environment. In yet another terminal, run the following:

```bash
cd art-deco-client
npm install
```

Then run the `dev` target in [packages.json](art-deco-client/package.json):

```bash
npm run dev
```


### Run the loader (not recommended)

The loader has already been run for you so you don't really need to do anything here. However, if you want to run it, you'll need to set up your Python environment. So, in a new terminal, run the following:

```bash
cd art-deco-loader
python3.12 -m venv venv
pip install -r requirements.txt
source venv/bin/activate
```

From here you can then run it. It's hard-coded to read the file [artwork-data.csv](art-deco-loader/artwork-data.csv) and to call the server on localhost and port 8000. Change it as you need and then run it:

```bash
python loader.py
```

Note that to load the entire file will take some time as it needs to download about 120,000 images and create embeddings for this. It took several hours on my Intel-based MacBoook Pro.


## Using the demo

In the left pane, you can upload an image with the "Choose File" button. There are some images to choose from in the [images](images) folder or just pick something from your machine. Nothing is stored so you can use whatever you like.

Then, click the "Find Artwork" button and the applicaiton will ask Redis to find the four-closest matches from the 120,000 embeddings stored, download the images from the [National Gallery of Art](https://www.nga.gov/), and present them to you.
