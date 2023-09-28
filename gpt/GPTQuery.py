from gpt.GPTBase import GPTBase


class GPTQuery(GPTBase):
    def __init__(self, system_prompt="You are a helpful AI", available_tools=None):
        super().__init__(system_prompt=system_prompt)
        self.system_prompt = system_prompt
        self.available_tools = available_tools or []

    def group_articles(self, articles, temperature=0):

        prompt = f"""
        Given the following news article titles and corresponding ID, group together the similar topics.
        Articles: 
        {articles}

        Answer in json only with the following format:
        {{similar_articles: [{{theme: <theme>, "similar_articles":[1,2]}}, {{theme: <theme>, "similar_articles":[3,4]}}]}}

        """
        
        res = self.generate_message(prompt, temperature)
        print(res)
        return res

    def ask(self, user_query, temperature=0):

        prompt = f"""
        {self.system_prompt}
        
        User: {user_query}

        """

        return self.generate_message(prompt, temperature)