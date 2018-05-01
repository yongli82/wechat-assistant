// pages/album/view.js
var app = getApp();
var page = 1;
var hadLastPage = false;

Page({

  /**
   * 页面的初始数据
   */
  data: {
    album_id: 0,
    photos: []
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.setData({
      album_id: options.id
    });
    page = 1;
    hadLastPage = false;
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
    //load
    this.loadList();
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },

  loadList: function () {
    if (hadLastPage != false) {
      wx.showToast({
        title: '到底了',
      })
      return;
    }

    var that = this;
    wx.request({
      method: 'GET',
      url: app.globalData.baseUrl + '/api/photo-items',
      data: {
        fields: 'id,name,description,type',
        album_id: that.data.album_id,
        expand: 'photos',
        page: page
      },
      header: {
        'content-type': 'application/json'
      },
      success: function (res) {
        var listData = that.data.photos;
        for (var i = 0; i < res.data.length; i++) {
          var photo_group = res.data[i]
          for (var j = 0; j < photo_group.photos.length; j++){
            var photo = photo_group.photos[j]
            if(!photo.path.startsWith("http")){
              photo.path = app.globalData.baseUrl + photo.path
            }
          }
          listData.push(photo_group);
        }

        if (res.header["X-Pagination-Page-Count"] == res.header["X-Pagination-Current-Page"]) {
          hadLastPage = res.header["X-Pagination-Current-Page"];
        } else {
          page++;
        }

        that.setData({
          photos: listData
        });
      },
    })
  },
  previewImage: function(event){
    console.log(event);
    var current_url = event.target.dataset.current_url;
    var that = this;
    var listData = that.data.photos;
    var urls = []
    for(var i=0; i < listData.length; i++){
      var photo_group = listData[i];
       for (var j = 0; j < photo_group.photos.length; j++) {
         var photo = photo_group.photos[j]
         urls.push(photo.path);
       }
    }
    wx.previewImage({
      urls: urls,
      current: current_url
    })
  }
})
