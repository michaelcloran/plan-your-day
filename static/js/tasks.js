//tasks
const editTaskModal = new bootstrap.Modal(document.getElementById("editTaskModal"));
const editTasksButtons = document.getElementsByClassName("btn-edit-task");

const editConfirm = document.getElementById("update");
const editCancel = document.getElementById("cancel");

const deleteTaskButtons = document.getElementsByClassName("btn-delete-task");
const deleteTaskModal = new bootstrap.Modal(document.getElementById("deleteTaskModal"));

for (let button of editTasksButtons){
button.addEventListener("click", (e) => {

  let taskId = e.target.getAttribute("data-task_id");

    editTaskModal.show();

    let parent = e.target.parentElement;

    let category = parent.getElementsByClassName("task-category")[0].innerText;

    let category_el = document.getElementById("id_category_id");
    for(let i=0; i< category_el.options.length; i++){
      if(category_el.options[i].text === category){
        category_el.options[i].selected = true;//'selected';
      }
    }

    let task_name_el = parent.getElementsByClassName('task-name');

    document.getElementById("id_task_name").value = task_name_el[0].innerText;

    let task_description_el = parent.getElementsByClassName('task-description');

    document.getElementById("id_task_description").value = task_description_el[0].innerText;

    let task_date_el = parent.getElementsByClassName('task-date');

    document.getElementById("id_date").value = task_date_el[0].innerText;

    let task_start_el = parent.getElementsByClassName('task-start');

    document.getElementById("id_start_time").value = task_start_el[0].innerText;


    let task_end_el = parent.getElementsByClassName('task-end');

    document.getElementById("id_end_time").value = task_end_el[0].innerText;

    editConfirm.addEventListener("click", (e) => {

      if (!editTaskForm.checkValidity()) {

        e.preventDefault();
        e.stopPropagation();

      }else{

        editTaskForm.action=`edit_task/${taskId}`;

        editTaskForm.submit();
      }
    });
    editCancel.addEventListener("click", (e) => {

      editTaskForm.submit();
    });
});
}

for (let button of deleteTaskButtons) {
  button.addEventListener("click", (e) => {
    let parent = e.target.parentElement;
    let task_date_el = parent.getElementsByClassName('task-date');

    let view_date = task_date_el[0].innerText;

    let todays_date = new Date();
    let year = todays_date.getFullYear();
    let month = String(todays_date.getMonth() + 1).padStart(2, '0');
    let day = String(todays_date.getDate()).padStart(2, '0');

    todays_date = year+"-"+month+"-"+day;

    let taskId = e.target.getAttribute("data-task_id");

    if(todays_date === view_date){
      deleteTaskConfirm.href = `delete_task/${taskId}`;
    }else{
      let index_of_date = window.location.href.indexOf(view_date);
      if(index_of_date == -1){
        deleteTaskConfirm.href = `${view_date}/delete_task/${taskId}`;
      }else{
        deleteTaskConfirm.href = `delete_task/${taskId}`;
      }
    }


    deleteTaskModal.show();
  });
}