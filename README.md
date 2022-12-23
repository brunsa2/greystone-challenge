# Greystone Challenge
In addition to commits, please review issues and merge requests which were used
to track pieces of work.

## Notes on amortization calculator
The amortization schedule generator calculates the payment using the traditional
formula but then derives a whole-cent payment. Since payments can only be with
whole cents, this will add a small discrepancy at the end which is corrected.
Given negative amortization, this will effectively create a balloon payment to
fully amortize the loan.

There might be methods to better calculate payment amounts to ensure more
similarity between regular monthly payments and the final payment (and also
handle the unevenness in payment periods due to differing length months), but
these were not implemented here (previous company I worked for used Newton's
method to calculate amortization schedules). The method used here is similar
to a spreadsheet calculation and should still produce good results.

## What is omitted
Security was not considered in this API (no authentication/authorization is
provided).

Transactions were not considered as the application was developed only with
in-memory repositories.

Some URL checks such as users belonging to a user were not provided—they are
present to complete the URL scheme and might in a more complex application
invoke authorization code.