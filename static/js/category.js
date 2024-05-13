
const categoryForm = document.getElementById("categoryForm");
const submitButton = document.getElementById("submitButton");

const editModal = new bootstrap.Modal(document.getElementById("editModal"));
const editButtons = document.getElementsByClassName("btn-edit");
const editConfirm = document.getElementById("update");
const editCancel = document.getElementById("cancel");
const categoryText = document.getElementById("id_category_name");

const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
const deleteButtons = document.getElementsByClassName("btn-delete");
const deleteConfirm = document.getElementById("deleteConfirm");


/**
* Initializes edit functionality for the provided edit buttons.
*
* For each button in the `editButtons` collection:
* - Retrieves the associated comment's ID upon click.
* - Fetches the content of the corresponding category.
* - Populates the `categoryText` input/textarea with the category's content for editing.
* - Updates the submit button's text to "Update".
* - Sets the form's action attribute to the `edit_category/{categoryId}` endpoint.
*/
for (let button of editButtons) {
button.addEventListener("click", (e) => {

    let categoryId = e.target.getAttribute("data-category_id");

    let categoryContent = document.getElementById(`category${categoryId}`).innerText;
    editModal.show();

    categoryText.value = categoryContent;

    editConfirm.addEventListener("click", (e) => {
      if (!editForm.checkValidity()) {

        e.preventDefault();
        e.stopPropagation();
      }else {
        editForm.action=`edit_category/${categoryId}`;

        editForm.submit();
      }
    });
    editCancel.addEventListener("click", (e) => {
      console.log("cancel clicked");
      //editForm.submit();
      editModal.hide();
      editModal.reset();
    });
  });
}

/**
* Initializes deletion functionality for the provided delete buttons.
*
* For each button in the `deleteButtons` collection:
* - Retrieves the associated categories ID upon click.
* - Updates the `deleteConfirm` link's href to point to the
* deletion endpoint for the specific category.
* - Displays a confirmation modal (`deleteModal`) to prompt
* the user for confirmation before deletion.
*/
for (let button of deleteButtons) {
    button.addEventListener("click", (e) => {
      let categoryId = e.target.getAttribute("data-category_id");
      deleteConfirm.href = `delete_category/${categoryId}`;
      deleteModal.show();
    });
}
