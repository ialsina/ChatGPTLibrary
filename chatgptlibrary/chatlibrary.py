import json
from datetime import datetime
import pandas as pd
from pathlib import Path

from .chat import Chat

class ChatLibrary:
    _columns = ("title", "conversation", "created", "updated")

    def __init__(self, data: str | Path | pd.DataFrame):
        if isinstance(data, (str, Path)):
            file = data
            df = pd.DataFrame(
                [self._parse(conversation) for conversation in self._read(file)]
            )
        elif isinstance(data, pd.DataFrame):
            df = data
        else:
            raise TypeError(
                "ChatLibrary must be initialized with str, Path or pd.DataFrame, "
                f"not {type(data).__name__}."
            )
        self._validate_df(df)
        self.df = df

    def __getitem__(self, key: int | slice | list[int] | str):
        if isinstance(key, str):
            return ChatLibrary(self.df[self.df["title"] == key])
        if isinstance(key, int):
            return ChatLibrary(pd.DataFrame([self.df.iloc[key]]))
        if isinstance(key, (slice, list, int)):
            return ChatLibrary(pd.DataFrame(self.df.iloc[key]))
        raise TypeError(
            "ChatLibrary index must be int, slice, list[int] or str, "
            f"not {type(key).__name__}."
        )

    def __len__(self):
        return len(self.df)

    def __repr__(self):
        return f"ChatLibrary[{len(self)}]"

    @staticmethod
    def _read(file):
        with open("conversations.json", "r") as rf:
            return json.load(rf)

    @staticmethod
    def _parse(conversation):
        content = []
        title = conversation["title"]
        for key, dct in conversation["mapping"].items():
            if dct.get("message") is None:
                continue
            role = dct["message"].get("author", {}).get("role", "unknown")
            if role == "system":
                continue
            if dct["message"].get("content") is None:
                continue
            if dct["message"]["content"].get("parts") is None:
                continue
            if role == "tool":
                content.append((role, []))
            else:
                content.append((role, dct["message"]["content"]["parts"]))
        return {
            "title": title,
            "conversation": content,
            "created": datetime.fromtimestamp(conversation["create_time"]),
            "updated": datetime.fromtimestamp(conversation["update_time"]),
        }

    @classmethod
    def _validate_df(cls, df):
        if sorted(df.columns) == sorted(cls._columns):
            return
        raise ValueError("Invalid DataFrame columns.")

    @property
    def title(self):
        return list(self.df.title)

    @property
    def conversation(self):
        return list(self.df.conversation)

    def grep(self, s: str):
        df = self.df
        filtered = df[
            df["conversation"].apply(
                lambda x: any(
                    any(s.lower() in message.lower() for message in messages)
                    for (_, messages) in x
                )
            )
        ]
        return ChatLibrary(filtered)

    def grepall(self, *args: str):
        if not args:
            return self
        result = self.grep(args[0])
        for s in args[1:]:
            result = result.grep(s)
        return result

    def grepany(self, *args: str):
        if not args:
            return ChatLibrary(pd.DataFrame(columns=self._columns))
        result = self.grep(args[0])
        for s in args[1:]:
            result = ChatLibrary(
                pd.concat([result.df, self.grep(s).df]).drop_duplicates()
            )
        return result
