// Файл worker.js

// Функция start
async function start() {
  let gpt_request = false;
  let gpt_code = false;
  let google_request = false;
  let dialog = false;
  let is_active_command = false;
  let weather = false;

  await eel.main(gpt_request, gpt_code, google_request, dialog, is_active_command, weather);
}

// Выполнение функции start
start()
  .then(() => {
    // Отправка сообщения об успешном выполнении в основной поток
    postMessage('start выполнена успешно');
  })
  .catch(error => {
    console.error('Ошибка:', error);
  });
