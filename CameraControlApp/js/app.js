function message(icon, message, fadeout) {
    var template = $('#alert-message-template').html();
    var html = Mustache.to_html(template, { icon: icon, message:message });
    $('#alert').html(html);
    $('#alert').show();
    if ( typeof(fadeout) != 'undefined' && fadeout == true )
        $('#alert').delay(1200).fadeOut('slow');
}

var CameraModel = Backbone.Model.extend({

});

var SideBar = Backbone.View.extend({

    el: $('#sidebar'),

    events: {
        'click #shot-button': 'shot',
        'click #poweroff-button': 'poweroff',
        'click #toggle-button': 'toggle'
    },

    initialize: function() {
        _.bindAll(this, 'shot', 'poweroff');
    },

    shot: function() {
        message('icon-camera', 'Taking picture...');
        $.ajax({
            url: '/services/shot',
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                    var template = $('#picture-template').html();
                    var html = Mustache.to_html(template, data);
                    $('#picture').html(html);
                    $('#alert').fadeOut('slow');
                } else {
                    $('#alert').hide();
                    message('icon-exclamation-sign', data.message, true);
                }
            }
        });
    },

    poweroff: function() {
        message('icon-remove-circle', 'Powering off...');
        $.ajax({
            url: '/services/poweroff',
            dataType: 'json',
            success: function(data) {
                if (!data.success) {
                    $('#alert').hide();
                    message('icon-exclamation-sign', data.message, true);
                }
            }
        });
    },

    toggle: function() {
        $('#sidebar #toggle-button').toggleClass('close');
        $('#sidebar .container').toggleClass('close');
    }

});


var Footer = Backbone.View.extend({

    el: $('#footer ul.thumbnails'),

    events: {
        'click li': 'open'
    },

    initialize: function() {
        _.bindAll(this, 'open', 'load');
        this.load();
    },

    open: function(ev) {
        //message('icon-camera', 'Open picture...', true);
        var filename = $(ev.target).attr('src');
        var template = $('#picture-template').html();
        var html = Mustache.to_html(template, {filename: filename});
        $('#picture').html(html);
        $("#picture img").imageZoom({scrollSensitivity: 0.01});
    },

    load: function() {
        var that = this;
        $.ajax({
            url: '/services/images-list',
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                    var template = $('#thumbnail-template').html();
                    var html = Mustache.to_html(template, data);
                    $(that.el).html(html);
                }
            }
        });
    }

});

var isMobile = false;
/*
var source = new EventSource('/services/stream');
    source.onmessage = function (event) {
        var data = JSON.parse(event.data);

        if (typeof (data.message) != 'undefined') {
            message('icon-camera', data.message, true);
        }
};
*/

$(document).ready(function() {
    //message('icon-camera', 'Camera connected');
    var sideBar = new SideBar();
    var footer = new Footer();

    var isMobile = navigator.userAgent.match(/Mobile/i) == true;

});