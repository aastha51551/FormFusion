from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from protocols.query import query_proto, QueryFormRequest, QueryFormResponse, FormStatus, GetTotalQueries, TotalQueries

user = Agent(
    name="user",
    port=8000,
    seed="user secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

fund_agent_if_low(user.wallet.address())

user.include(query_proto)

# Query for a non-existent form title
Form_query = QueryFormRequest(
    body="UGAC",
    title="Non-existent Form Title",
)

# Handle the query response
@user.on_message(QueryFormResponse)
async def handle_query_response(ctx: Context, sender: str, msg: QueryFormResponse):
    if msg.forms:
        # Log and handle the form details if found
        print(f"Received form details: {msg.forms}")
        await submit_form(ctx, msg.forms)
    else:
        # Log and handle the case where form is not found
        print(f"Form with title '{Form_query.title}' not found.")
        # Handle the response appropriately, e.g., update logs or notify user

async def submit_form(ctx: Context, form_details: FormStatus):
    # Implementation of form submission logic
    pass

# Perform the query at regular intervals
@user.on_interval(period=5.0, messages=QueryFormRequest)
async def interval(ctx: Context):
    completed = ctx.storage.get("completed")
    if not completed:
        await ctx.send("organisation_address_here", Form_query)

if __name__ == "__main__":
    user.run()
