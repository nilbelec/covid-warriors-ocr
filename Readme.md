# COVID-Warriors OCR
Heroku OCR web application to support [COVID-Warriors](https://covidwarriors.io) projects.

## Quick Deploy
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## Configuration
This application uses the "heroku-community/apt" buildpack to install tesseract and its trained data for Spanish and English languages.

Please, double check the TESSDATA_PREFIX environment variable is correctly pointing to the "tessdata" folder.

## Licence
MIT Licence. Copyright (c) 2020 Juan Álvarez