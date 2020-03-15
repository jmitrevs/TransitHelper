# TransitHelper

An application to estimate transit time taking into account
uncertainties. This is mainly useful for routes with transfers. The
motivation is that sometimes a particular route is nominally the
fastest, but if a connection is missed, the wait time is long. A route
that may be nominally slower but that has a smaller penalty if a
connection is missed may be preferrable. This is why it often makes
sense to just take frequent buses even if a connection to an
infrequent bus may be faster. Google does not seem to take into
account uncertainties very well, so I wanted to 

This makes use of the Chicago Transit Authority (CTA) Bus Tracker
information. One must request a token from the CTA to access the
tracker via the web interface. In a Tokens.py file in the
TransitHelper directory one should define a constant BUS_TOKEN to
refer to the token.

The current usage is quite basic, and requires a list of bus
stations for the routes. There is no suggesting of routes
capability. The main function is `PredictTripTime` in
`PredictTime.py`. Most of the testing/development is being done using the
jupyter notebook.

The `tests` directory provides unit tests.
