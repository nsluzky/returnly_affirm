Assignment:
Write a functional test plan for shopping workflow in a TESTPLAN.md file and sort the test with the highest priority at the top. The scope of this is just the flow of buying an item from the UI.

Goals:
Pinpoint areas of testing that can impact customer satisfaction in the worst way.

I consider the following areas as the highest priority:
    Service unavailability including but not limited to server crushes and slow response
    Failure to place order
    Failure to find requested product
    Wrongfully placed order: wrong product, location, without confirmation, wrongly calculated price
    Order was changed without notification, for example, price, or size, or description changed or item is removed 
    Over-complicated design when it's hard to find "way-to-go"
    Allowing customers making "wrong choices" rather than providing only valid choices.
        For example, button "Continue" should be enabled only after all required fields are filled and all validations on the page are verified.

I'd suggest the following P1 tests to be included in the Test Plan
For every webpage validate that:
    all major fields are visible and enabled
    "Continue" or "Next step button" is enabled (or becomes visible) only after all validations on the page pass
    All failed validations are clearly explained
Have end-to-end tests for all frequently-usable user scenarios including but not limited to:
    Search for a product, use By It Now, potentially change quality, complete order or drop it
    Search for a product, use add to shopping card, potentially change quality, complete order or drop it, or continue shopping
    Execute same scenarios with first adding a few new products and then removing them
    Execute same scenarios with first adding a few new products, adding them to shopping card, and then removing before order was completed - customer should be warned
    Same scenarios when products' parameters AND ESPECIALLY PRICE(!) have changed

EVERY backend action including ones launched from frontend should be thorougly tested
to make sure that data is consistent, server is not impacted, and performance is as expected.

For example, for products we'd better to validate that:
    Adding products with invalid descriptions or duplicated ones doesn't happen
    Product's info matches the input data
    Added products are in the backend system and are visible from frontend

To allow tests running concurrently by multiple manual and automated testers without impacting each other,
tests should use existing data only as read-only. 
To test adding, modifying and removing any info: products, orders, customers, categories - new entities should be created at tests' setup and then removed at tearDown

It's also highly recommended randomizing testing scenario by selecting as much as possible randomly.
For example, while selecting a product on a page to purchase, select it randomly, select both existing and newly added products, select quantity randomly,
select number of other products to be added to shopping card randomly, ...

I'd suggest having a separate set of tests validating that frontend matches backend.
For example, when products are added, deleted, and modified it's properly and timely reflected on frontend.
Info should be auto-refreshed
If products are in shopping list, customers should be notified of the changes 
