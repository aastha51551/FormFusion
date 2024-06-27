from protocols.submission import SubmitFormRequest, SubmitFormResponse
from protocols.query import (
    QueryFormRequest,
    QueryFormResponse,
)
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
 
ORGANISATION_ADDRESS = "agent1qw50wcs4nd723ya9j8mwxglnhs2kzzhh0et0yl34vr75hualsyqvqdzl990"
 
user = Agent(
    name="user",
    port=8000,
    seed="user secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)
 
fund_agent_if_low(user.wallet.address())
 
Form_query = QueryFormRequest(
    title="Internship Session"
)

@user.on_interval(period=5.0, messages=QueryFormRequest)
async def interval(ctx: Context):
    completed = ctx.storage.get("completed")
 
    if not completed:
        await ctx.send(ORGANISATION_ADDRESS, Form_query)
 
