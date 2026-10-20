from ai.llm.nvidia import NVIDIAProvider


class ChatOrchestrator:
    def __init__(self, provider=None):
        self.provider = provider or NVIDIAProvider()

    def build_prompt(self, question: str, context: str | None = None) -> str:
        if context:
            return (
                "Use the context below to answer the user question. "
                "If the answer is not in the context, say that the information "
                "is not available in the provided institutional material.\n\n"
                f"Context:\n{context}\n\nQuestion:\n{question}"
            )

        return (
            "Answer the question as helpfully as possible. "
            "If you are unsure or the answer is not supported by the available "
            "knowledge, say so clearly.\n\n"
            f"Question:\n{question}"
        )

    def answer(self, question: str, context: str | None = None) -> str:
        prompt = self.build_prompt(question, context)
        return self.provider.generate(prompt)