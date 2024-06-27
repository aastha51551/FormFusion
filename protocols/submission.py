from uagents import Context, Model, Protocol
from .query import FormStatus
from typing import List

class SubmitFormRequest(Model):
    title: str
    fields: List[str]

class SubmitFormResponse(Model):
    success: bool

submit_proto = Protocol()

@submit_proto.on_message(model=SubmitFormRequest, replies=SubmitFormResponse)
async def handle_submit_request(ctx: Context, sender: str, msg: SubmitFormRequest):
    forms = {
        num: FormStatus(**status)
        for num, status in ctx.storage._data.items()
        if status['title'] == msg.title
    }
    
    if not forms:
        await ctx.send(sender, SubmitFormResponse(success=False))
        return
    
    
    submission_data = {
        'title': msg.title,
        'fields': msg.fields
    }
    
    await ctx.send(sender, SubmitFormResponse(success=True))
