# `wiringPiD/network.h`

Python-модуль: `wiringop.wiring_pi_d.network`.

Модуль зеркально покрывает публичный API заголовка wiringOP. Имена Python приведены к Python-стилю; рядом сохраняются C-имена для однозначного сопоставления.

## Функции

- `getClientIP` → `get_client_ip()`; C return `char *`; адаптация `direct`.
- `getResponce` → `get_response_legacy(client_fd)`; C return `int`; адаптация `legacy_typo`.
- `setupServer` → `setup_server(server_port)`; C return `int`; адаптация `direct`.
- `sendGreeting` → `send_greeting(client_fd)`; C return `int`; адаптация `direct`.
- `sendChallenge` → `send_challenge(client_fd)`; C return `int`; адаптация `direct`.
- `getResponse` → `get_response(client_fd)`; C return `int`; адаптация `direct`.
- `passwordMatch` → `password_match(password)`; C return `int`; адаптация `direct`.
- `closeServer` → `close_server(client_fd)`; C return `void`; адаптация `direct`.

