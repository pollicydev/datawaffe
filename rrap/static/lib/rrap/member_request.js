$(function () {
  $(".request-actions button").click(function () {
    var btn = $(this);
    var request_actions = $(this).closest(".request-actions");
    var organization_id = $(request_actions).attr("data-organization-id");
    if ($(request_actions).hasClass("request_membership")) {
      $.ajax({
        url: "/organizations/membership/request/",
        data: { "organization-id": organization_id },
        type: "get",
        cache: false,
        beforeSend: function () {
          $(btn).attr("disabled", true);
        },
        success: function (data) {
          $(btn).removeClass("btn-secondary");
          $(btn).addClass("btn-info");
          $(btn).html(
            "<span class='icon mdi mdi-check-circle'></span> Request Sent"
          );
        },
        error: function (jqXHR, textStatus, errorThrown) {},
        complete: function () {
          $(btn).attr("disabled", false);
        },
      });
    }
  });
});
