RushedSearch
Clifford Lau 995435480

--Introducton--
I had the good fortune to be somewhat familiar with the concepts required to implement this project.  Unfortunately, the partner I had previously made arrangements with had reconsidered his decision, and I was forced to complete the project myself. This, combined with limited time for completion made development difficult. As a result, the project is not at a level of completion I am satisfied with. With exception of pagerank, the individual components do work, and should integrate together. Aptly, Id have named it RushedSearch, as it a rushed piece of work. Apologies.


--Database--
I decided to go ahead and use the native sqlite3 support that python provides, as allowed for the least amount of time required for implementation. For db interaction, I decided to restrict all access to an external library class to be instantiated wherever needed.

The majority of the working logic for both the crawler and the search is implemented though the use of sql queries. This decision allowed me to encapsulate the organizational logic (i.e. finding and iterating through words on a page) and the data logic. In that sense, I simply need to call my db library with values, without having to worry about id keys. This method would also allow me to instantiate and use my db class in any file (i.e. in the crawler, the pagerank or the frontend) without having to use an id (and therefore break encapsulation). I chose to not build a cache, but instead rely on blind UPDATE OR IGNORE (on conflict) in consideration of the crawler being called with and without a clean database.

--Crawler--
The crawler was adapted from the one provided. I removed the caching, and simply inserted my own db functions where necessary. Very little extra work was required.


--Frontend--
The frontend is functional, with very little fluff. While the query form and submit is basic html, I needed to use the template function in order to lit the data properly. The form submits the query as a GET request back to the same page, which lists the results if a query GET request is provided. In summary, a single page and a signel route handler is all that is necessary.

--Page Rank--
I had trouble with the pagerank algorithm, and unfortunately ran out of time. I have very little to say about it.

--Testing--
I ran out of time required for testing, so this section is incomplete. Testing the database was straightforward, as all I had to do was make sure that the database operations I intended to happen actually happened.

--Final Thoughts--
Time was the only real issue here. Due to unforseen circumstances (having to complete the project on my own) and a limited time schedule, I had insufficient time to produce this. Still, I did the best I could given the situation.