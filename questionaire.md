# Questionaire
1. Are there any sub-optimal choices( or short cuts taken due to limited time ) in your implementation?
  - I wish I had not coupled the data information so closely with the structure of the page when designing the main template used for the site. Designing with more of an input-oriented mentality would have allowed me to more easily implement AJAX functionality, which in turn would have led to some cool additional features.
---
2. Is any part of it over-designed? ( It is fine to over-design to showcase your skills as long as you are clear about it)
  - I wasn’t sure if it was entirely necessary for this assignment but I implemented some encryption/decryption on the secret key for the API I utilized. This was to ensure that I wasn’t publishing a secret key into a public repository which is dangerous. I only implemented this on the secret key for the API, although I could have done something similar for the secret key for the Django project as well. I left the decryption key in the repository for simplicity on your end to test my product but in a proper implementation I would use some kind of secure key-sharing. 
  - I tried to follow some of the best-practices I’ve learned from my internship this past summer in my Github repository. Although it was just myself and I almost always just merged immediately due to time constraints, I wanted to at least demonstrate that I am comfortable and proficient in Git and Github. 
---
3. If you have to scale your solution to 100 users/second traffic what changes would you make, if any?

  - I think the efficiency of building the html page out of the template could be improved, mostly because of time constraints. I used four for loops, meaning that to build a single template takes time proportional to:
    ```
    (Number of coins being queried) x (Number of exchanges being checked) x (Number of offers being queried) x 2 
    ```
  - The efficiency of my recommendation algorithm should be optimal, seeing I implemented merge sort and that runs in time nlogn. However, the four for loops in the template would definitely be my first place of optimization. 
  - I would also take more time to ensure the security of the site was solid. Right now I encrypt the API’s secret key but also leave the decryption key for that in the Github repository, which isn’t secure and would lead to issues in a real deployment.
---
4. What are some other enhancements you would have made, if you had more time to do this implementation
  - As I mentioned before, had I designed with AJAX in mind I could have implemented some cool features. AJAX would allow for the exchange page to be loaded quicker and have the data eventually populate with a placeholder buffering gif rather than waiting for the entire page to generate. AJAX would also allow me to implement an auto-refresh functionality where the numbers and recommendations would refresh every 10 seconds or so. 
