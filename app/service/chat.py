from langchain_core.messages.ai import AIMessage
from langchain_core.messages.system import SystemMessage

from app.infrastructure.ia.openia_cli import OpenAICli


def start_chat() -> Exception | None:
    message = [
        SystemMessage("You area a Chat Assistant to response basic questions"),
        AIMessage("hello How Are you?"),
    ]
    try:
        llm = OpenAICli()
        while True:
            human = input("\nYou:")
            if human == "exit":
                print("Exiting chat...")
                break
            llm.history.add_message(AIMessage(human))
            response = llm.client.invoke(message)
            llm.history.add_message(AIMessage(response.content))

            print(llm.history.messages)
            print(response.content)
    except Exception as e:
        print(e)
        return e
