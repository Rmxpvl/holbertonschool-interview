# Star Wars API

Interview project: query the [Star Wars API](https://swapi-api.hbtn.io/api/) (SWAPI) to list information about a movie.

## Requirements

- Ubuntu 14.04 LTS, Node.js 10.14.x
- Code must be semistandard compliant (Standard + semicolons)
- All files must be executable and start with `#!/usr/bin/node`
- `var` is not allowed

## Setup

```
npm install
```

## Tasks

### 0. Star Wars Characters

`0-starwars_characters.js` - prints every character of a Star Wars movie, based
on the movie ID passed as an argument, in the order they are listed in the
movie's `characters` field.

```
./0-starwars_characters.js <movie_id>
```

Example:

```
./0-starwars_characters.js 3
Luke Skywalker
C-3PO
R2-D2
...
```
