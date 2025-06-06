from datetime import datetime
import json
from pathlib import Path
import tempfile
import os
import zipfile

import pandas as pd

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
            result = self.df[self.df["title"] == key]
            if len(result) == 1:
                return Chat.from_series(result.iloc[0])
            if len(result) == 0:
                raise KeyError(f"No chat with title '{key}' found.")
            return ChatLibrary(result)
        if isinstance(key, int):
            return Chat.from_series(self.df.iloc[key])
        if isinstance(key, (slice, list)):
            result = pd.DataFrame(self.df.iloc[key])
            if len(result) == 1:
                return Chat.from_series(result.iloc[0])
            return ChatLibrary(result)
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
        file = str(file)
        if file.endswith(".zip"):
            with tempfile.TemporaryDirectory() as tmpdir:
                with zipfile.ZipFile(file, "r") as zip_ref:
                    zip_ref.extractall(tmpdir)
                json_path = os.path.join(tmpdir, "conversations.json")
                with open(json_path, "r", encoding="utf-8") as rf:
                    return json.load(rf)
        else:
            with open(file, "r", encoding="utf-8") as rf:
                return json.load(rf)

    @staticmethod
    def _parse(conversation):
        content = []
        title = conversation["title"]
        for _, dct in conversation["mapping"].items():
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
            new_results = self.grep(s)
            combined_df = pd.concat([result.df, new_results.df])
            result = ChatLibrary(combined_df.drop_duplicates(subset=["title"]))
        return result
