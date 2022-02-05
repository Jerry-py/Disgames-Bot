import discord
from discord.ext import commands

class Dropdown(discord.ui.Select):
    """A Simple Dropdown View"""
    def __init__(self, placeholder: str, pages : list, pagination_type : str):
        self._pagination_type = pagination_type
        self._placeholder = placeholder
        self._pages = pages
        self._options = [
            discord.SelectOption(label=f"Page {int(page+1)}", description=f"Page {int(page+1)}")
            for page in range(len(pages))
        ]


        super().__init__(
            placeholder=self._placeholder,
            min_values=1,
            max_values=1,
            options=self._options,
        )

    async def callback(self, inter):
        page = self._pages[int(str(self.values[0]).replace("Page ", ""))-1]
        if self._pagination_type == 'embed':
            await inter.response.edit_message(embed=page)
        else:
            await inter.response.edit_message(content=page)

class EmbedPaginator(discord.ui.View):
    """A Simple Embed Paginator using discord Views"""
    def __init__(self, ctx : commands.Context, embeds : list, timeout : int = 120, dropdown : bool = True): 
        super().__init__(timeout=timeout)
        self.embeds = embeds
        self.ctx = ctx
        self.current_page = 0
        if dropdown:
            self.add_item(Dropdown('Select a page', self.embeds, 'embed'))

    async def show_page(self, inter, page: int):
        """Change the page of the paginator"""
        await inter.response.defer()
        self.current_page = 0 if page >= len(self.embeds) else page
        embed = self.embeds[self.current_page]
        await inter.edit_original_message(embed=embed)
        
    @discord.ui.button(label='⏪')
    async def beginning(self, button, inter):
        """Go to the first page"""
        await self.show_page(inter, 0)

    @discord.ui.button(label="⬅️")
    async def back(self, button, inter):
        """Go to the previous page"""
        await self.show_page(inter, self.current_page - 1)     

    @discord.ui.button(label="➡️")
    async def forward(self, button, inter):
        """Go to the next page"""
        await self.show_page(inter, self.current_page + 1)
        
    @discord.ui.button(label='⏩')
    async def end(self, button, inter):
        """Go to the last page"""
        await self.show_page(inter, -1)
        
    @discord.ui.button(label="Quit")
    async def quit(self, button, inter):
        """Quit the paginator"""
        await inter.response.defer()
        await inter.delete_original_message()    
        
    async def interaction_check(self, inter):
        """Check if the user who used the the interaction is the author of the message"""
        if inter.user == self.ctx.author:
            return True
        await inter.response.send_message("Hey! You can't do that!", ephemeral=True)
        return False
    
    async def on_timeout(self) -> None:
        """When the view times out"""
        self.clear_items()
    

class MessagePaginator(discord.ui.View): 
    """A Simple Message Paginator using discord Views"""
    def __init__(self, ctx : commands.Context, messages : list, timeout : int = 120, dropdown : bool = True): 
        super().__init__(timeout=timeout) 
        self.messages = messages
        self.ctx = ctx
        self.current_page = 0
        if dropdown:
            self.add_item(Dropdown('Select a page', self.messages, 'message'))

    async def show_page(self, inter, page: int):
        """Change the page of the paginator"""
        self.current_page = 0 if page >= len(self.messages) else page
        await inter.edit_original_message(content=self.messages[self.current_page])
        
    @discord.ui.button(label='⏪')
    async def beginning(self, button, inter):
        """Go to the first page"""
        await inter.response.defer()
        await self.show_page(inter, 0)

    @discord.ui.button(label="⬅️")
    async def back(self, button, inter):
        """Go to the previous page"""
        await inter.response.defer()
        await self.show_page(inter, self.current_page - 1) 

    @discord.ui.button(label="➡️")
    async def forward(self, button, inter):
        """Go to the next page"""
        await inter.response.defer()
        await self.show_page(inter, self.current_page + 1)
        
    @discord.ui.button(label='⏩')
    async def end(self, button, inter):
        """Go to the last page"""
        await inter.response.defer()
        await self.show_page(inter, -1)
        
    @discord.ui.button(label="Quit")
    async def quit(self, button, inter):
        """Quit the paginator"""
        await inter.response.defer()
        await inter.delete_original_message()   
        
    async def interaction_check(self, inter):
        """Check if the user who used the the interaction is the author of the message"""        
        if inter.user == self.ctx.author:
            return True
        await inter.response.send_message("Hey! You can't do that!", ephemeral=True)
        return False

    async def on_timeout(self) -> None:
        """When the view times out"""
        self.clear_items()