const express = require('express');
const app = express();
const port = 1905;
//Isso aqui fala pro back que os arquivos estão na msm pasta
app.use(express.static('./frontend'));


app.get('/', (req, res) => {
  res.sendFile(__dirname + '/frontend/index.html');
});

app.listen(port, () => {
  console.log(`Seu servidor esta rodando em: http://localhost:${port}`);
});