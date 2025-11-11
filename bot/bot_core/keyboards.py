class Keyboards:

    @staticmethod
    def pizza_selection():
        return {
            "inline_keyboard": [
                [
                    {"text": "🔴 Маргарита", "callback_data": "pizza_маргарита"},
                    {"text": "🌶️ Пепперони", "callback_data": "pizza_пепперони"},
                ],
                [
                    {"text": "🧀🧀🧀🧀 4 Сыра", "callback_data": "pizza_4_сыра"},
                    {"text": "🥓 Карбонара", "callback_data": "pizza_карбонара"},
                ],
                [
                    {"text": "🔥 Диабло", "callback_data": "pizza_диабло"},
                    {"text": "🥬 Веганская", "callback_data": "pizza_веганская"},
                ],
                [
                    {"text": "🍄 Грибная", "callback_data": "pizza_грибная"},
                    {
                        "text": "🦐 С морепродуктами",
                        "callback_data": "pizza_морепродукты",
                    },
                ],
            ]
        }

    @staticmethod
    def size_selection():
        return {
            "inline_keyboard": [
                [
                    {
                        "text": "👶 Маленькая (25cm)",
                        "callback_data": "size_small",
                    },
                    {
                        "text": "👦 Средняя (30cm)",
                        "callback_data": "size_medium",
                    },
                ],
                [
                    {
                        "text": "👨 Большая (35cm)",
                        "callback_data": "size_large",
                    },
                    {
                        "text": "🎪 Огромная (40cm)",
                        "callback_data": "size_xl",
                    },
                ],
            ]
        }

    @staticmethod
    def drinks_selection():
        return {
            "inline_keyboard": [
                [
                    {"text": "🔴 Coca-Cola", "callback_data": "drink_coca_cola"},
                    {"text": "🔵 Pepsi", "callback_data": "drink_pepsi"},
                ],
                [
                    {
                        "text": "🍊 Апельсиновый сок",
                        "callback_data": "drink_orange_juice",
                    },
                    {"text": "🍎 Яблочный сок", "callback_data": "drink_apple_juice"},
                ],
                [
                    {"text": "💧 Минеральная вода", "callback_data": "drink_water"},
                    {
                        "text": "🥤 Холодный чай Lipton",
                        "callback_data": "drink_iced_tea",
                    },
                ],
                [
                    {"text": "🚫 Без напитков", "callback_data": "drink_none"},
                ],
            ]
        }

    @staticmethod
    def order_confirmation():
        return {
            "inline_keyboard": [
                [
                    {"text": "✅ Всё верно", "callback_data": "order_approve"},
                    {"text": "🔄 Начать заново", "callback_data": "order_restart"},
                ],
            ]
        }

    @staticmethod
    def remove_keyboard():
        return {"remove_keyboard": True}
