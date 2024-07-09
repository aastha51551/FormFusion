from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from protocols.submission import SubmitFormRequest, SubmitFormResponse
from protocols.query import QueryFormRequest, QueryFormResponse, FormStatus, GetTotalQueries, TotalQueries

# Organisation agent address
ORGANISATION_ADDRESS = "agent1qw50wcs4nd723ya9j8mwxglnhs2kzzhh0et0yl34vr75hualsyqvqdzl990"

# Create an agent named "user" on port 8000 with a specific seed phrase
user = Agent(
    name="user",
    port=8000,
    seed="user secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

# Fund the agent's wallet if the balance is low
fund_agent_if_low(user.wallet.address())

# Define the form query request
form_query = QueryFormRequest(
    body="Please provide the form details",
    title="Internship Session",
)

# Function to submit the form once the form details are received
async def submit_form(ctx: Context, form_details: FormStatus):
    form_data = SubmitFormRequest(
        title=form_details.title,
        fields=["John Doe", "john@example.com", "123-456-7890", "Resume content here"]
    )
    await ctx.send(ORGANISATION_ADDRESS, form_data)

# Handle query form response
@user.on_message(QueryFormResponse)
async def handle_query_response(ctx: Context, sender: str, msg: QueryFormResponse):
    if msg.forms:
        print(f"Received form details: {msg.forms}")
        await submit_form(ctx, msg.forms)
    else:
        print("Form not found")

# Handle form submission response
@user.on_message(SubmitFormResponse)
async def handle_submit_response(ctx: Context, sender: str, msg: SubmitFormResponse):
    if msg.success:
        print("Form submitted successfully")
    else:
        print("Form submission failed")

# Handle total queries response
@user.on_message(TotalQueries)
async def handle_total_queries(ctx: Context, sender: str, msg: TotalQueries):
    print(f"Total queries made: {msg.total_queries}")

# Periodically send a form query request
@user.on_interval(period=5.0, messages=QueryFormRequest)
async def interval(ctx: Context):
    completed = ctx.storage.get("completed")
    if not completed:
        await ctx.send(ORGANISATION_ADDRESS, form_query)

# Query total queries made
async def query_total_queries(ctx: Context):
    await ctx.send(ORGANISATION_ADDRESS, GetTotalQueries())

# Run the agent
if __name__ == "__main__":
    user.run()
