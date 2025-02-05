update_user_balance_responses = {
    200: {
        "description": "Успешный запрос",
        "content": {
            "application/json": {
                "examples": {
                    "successful operation": {
                        "summary": "Баланс изменен",
                        "value": {
                            "status": "success",
                            "message": "Баланс пользователя успешно обновлен",
                            "user": {
                                "id": 1,
                                "username": "example_user",
                                "telegram_id": 123456789,
                                "balance": 100,
                                "role": "USER",
                                "done_tasks": 10,
                                "group_number": "1A",
                            },
                        },
                    }
                }
            }
        },
    },
    401: {
        "description": "Пользователь не авторизован",
        "content": {
            "application/json": {
                "examples": {
                    "not_authorized": {
                        "summary": "JWT-токен отсутствует или невалиден",
                        "value": {"detail": "Не авторизован"},
                    }
                }
            }
        },
    },
    404: {
        "description": "Пользователь не найден",
        "content": {
            "application/json": {
                "examples": {
                    "user_not_found": {
                        "summary": "Пользователь не найден в базе данных",
                        "value": {"detail": "Пользователь не найден"},
                    }
                }
            }
        },
    },
    500: {
        "description": "Внутренняя ошибка сервера",
        "content": {
            "application/json": {
                "examples": {
                    "unexpected_error": {
                        "summary": "Неожиданная ошибка",
                        "value": {
                            "detail": "Произошла непредвиденная ошибка: <тип ошибки>"
                        },
                    }
                }
            }
        },
    },
}

base_bad_response_for_endpoints_of_task = {
    401: {
        "description": "Пользователь не авторизован",
        "content": {
            "application/json": {
                "examples": {
                    "not_authorized": {
                        "summary": "JWT-токен отсутствует или невалиден",
                        "value": {"detail": "Не авторизован"},
                    }
                }
            }
        },
    },
    404: {
        "description": "Пользователь не найден",
        "content": {
            "application/json": {
                "examples": {
                    "user_not_found": {
                        "summary": "Задача не найдена в базе данных",
                        "value": {"detail": "Пользователь не найден"},
                    }
                }
            }
        },
    },
    500: {
        "description": "Внутренняя ошибка сервера",
        "content": {
            "application/json": {
                "examples": {
                    "unexpected_error": {
                        "summary": "Неожиданная ошибка",
                        "value": {
                            "detail": "Произошла непредвиденная ошибка: <тип ошибки>"
                        },
                    }
                }
            }
        },
    },
}
