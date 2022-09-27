$(function () {
  $.fn.updateFollowersCount = function (organization_id) {
    var container = $(this);
    $.ajax({
      url: "/activity/update_followers_count/",
      data: { "organization-id": organization_id },
      type: "get",
      cache: false,
      success: function (data) {
        $(container).text(data);
      },
    });
  };

  $(".user-actions button").click(function () {
    var btn = $(this);
    var user_actions = $(this).closest(".user-actions");
    var organization_id = $(user_actions).attr("data-organization-id");
    // Unfollow action
    if ($(user_actions).hasClass("following")) {
      $.ajax({
        url: "/activity/unfollow/",
        data: { "organization-id": organization_id },
        type: "get",
        cache: false,
        beforeSend: function () {
          $(btn).attr("disabled", true);
        },
        success: function (data) {
          $(user_actions).removeClass("following");
          $(user_actions).addClass("not-following");
          $(btn).removeClass("btn-danger");
          $(btn).addClass("btn-success");
          $(btn).html("<span class='icon mdi mdi-check-circle'></span> Follow");
          if ($(user_actions).hasClass("update-count")) {
            $(".followers-count").updateFollowersCount(organization_id);
          }
        },
        error: function (jqXHR, textStatus, errorThrown) {},
        complete: function () {
          $(btn).attr("disabled", false);
        },
      });
    }
    // Follow action
    else {
      $.ajax({
        url: "/activity/follow/",
        data: { "organization-id": organization_id },
        type: "get",
        cache: false,
        beforeSend: function () {
          $(btn).attr("disabled", true);
        },
        success: function (data) {
          $(user_actions).removeClass("not-following");
          $(user_actions).addClass("following");
          $(btn).removeClass("btn-success");
          $(btn).addClass("btn-danger");
          $(btn).html(
            "<span class='icon mdi mdi-minus-circle'></span> Unfollow"
          );
          if ($(user_actions).hasClass("update-count")) {
            $(".followers-count").updateFollowersCount(organization_id);
          }
        },
        error: function (jqXHR, textStatus, errorThrown) {},
        complete: function () {
          $(btn).attr("disabled", false);
        },
      });
    }
  });
});
