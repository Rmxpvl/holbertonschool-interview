#!/usr/bin/node
const request = require('request');

const movieId = process.argv[2];
const filmUrl = `https://swapi-api.hbtn.io/api/films/${movieId}/`;

request(filmUrl, (err, res, body) => {
  if (err) return;
  const characters = JSON.parse(body).characters;

  const results = [];
  let done = 0;

  characters.forEach((url, i) => {
    request(url, (err, res, body) => {
      if (err) return;
      results[i] = JSON.parse(body).name;
      done++;
      if (done === characters.length) {
        results.forEach(name => console.log(name));
      }
    });
  });
});
