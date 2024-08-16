document.addEventListener("DOMContentLoaded", function () {
    const filterButtons = document.querySelectorAll(".filter-button");
    const galleryItems = document.querySelectorAll(".gallery-item");

    // Initially display all items
    filterButtons.forEach(btn => {
      if (btn.getAttribute("data-filter") === "all") {
        btn.classList.add("btn-primary");
      } else {
        btn.classList.add("btn-secondary");
      }
    });

    galleryItems.forEach(item => {
      item.style.display = "block"; // Show all items by default
    });

    // Filter items based on button click
    filterButtons.forEach(button => {
      button.addEventListener("click", () => {
        const filter = button.getAttribute("data-filter");

        // Reset all buttons to secondary, set clicked button to primary
        filterButtons.forEach(btn => btn.classList.remove("btn-primary"));
        filterButtons.forEach(btn => btn.classList.add("btn-secondary"));
        button.classList.remove("btn-secondary");
        button.classList.add("btn-primary");

        // Show or hide items based on the filter
        galleryItems.forEach(item => {
          const category = item.getAttribute("data-category");
          if (filter === "all" || category === filter) {
            item.style.display = "block";
          } else {
            item.style.display = "none";
          }
        });
      });
    });
  });