// pages/photo/add.js
var app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    currentPhoto: false,
    albumIndex: -1,
    album_id: null,
    albums: [],
    photos: [],
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log("options:");
    console.log(options);
    if (options.album_id){
    this.setData({
      album_id: options.album_id
    });
  }
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
    var that = this;
    wx.request({
      method: 'GET',
      url: app.globalData.baseUrl + '/api/albums',
      data: {
        fields: 'id,name'
      },
      header: {
        'content-type': 'application/json'
      },
      success: function (res) {
        var albums = res.data
        that.setData({
          albums: albums
        });
        console.log("current album id=" + that.data.album_id);
        if (that.data.album_id){
          
          for (var i = 0; i < albums.length; i++) {
            var album = albums[i];
            if (album.id == that.data.album_id){
              that.setData({
                albumIndex: i
              });
              console.log("current album index=" + i);
              break;
            }
          }
        }
      },
    })
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

  /**
   * 上传图片
   */
  chooseImage: function () {
    var that = this;
    var items = that.data.photos;
    wx.chooseImage({
      count: 9, // 默认9
      sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
      sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
      success: function (res) {
        // 返回选定照片的本地文件路径列表，tempFilePath可以作为img标签的src属性显示图片
        var tempFilePaths = res.tempFilePaths;

        for (var i = 0; i < tempFilePaths.length; i++) {
          items.push({
            src: tempFilePaths[i]
          });
        }

        that.setData({
          photos: items
        });
      }
    })
  },

  previewImage: function (e) {
    var current = e.target.dataset.src

    wx.previewImage({
      current: current,
      urls: this.data.photos
    })
  },

  /**
   * 提交表单
   */
  formSubmit: function (e) {
    var that = this;
    var desc = e.detail.value.desc;
    if (that.data.albumIndex < 0) {
      wx.showToast({
        title: '请选择相册',
      })
      return;
    }
    var albumId = that.data.albums[that.data.albumIndex].id;

    if (that.data.photos.length == 0) {
      wx.showToast({
        title: '至少传一个图',
      })
      return;
    }


    wx.showLoading({ title: '提交中' });
    wx.request({
      method: 'POST',
      data: {
        album_id: albumId,
        description: desc
      },
      url: app.globalData.baseUrl + '/api/photos',
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
      success: function (res) {

        if (res.statusCode == 201) {
          // 成功了
          var photos = that.data.photos;
          for (var i = 0; i < photos.length; i++) {
            wx.showLoading({ title: '上传中' + (i + 1) });
            that.uploadImage(res.data, photos[i]);
          }

          wx.hideLoading();
          wx.showModal({
            title: app.globalData.appName,
            content: '发布照片成功',
            cancelText: '继续上传',
            confirmText: '返回相册',
            success: function (r) {
              if (r.confirm) {
                  wx.navigateTo({
                    url: '/pages/album/view?id=' + albumId,
                  })
              } else if (r.cancel) {

                that.setData({
                  photos: []
                });
              }
            }
          })
        } else {
          wx.showModal({
            title: app.globalData.appName,
            content: res.data
          })
          wx.hideLoading();
        }
      }
    });
  },

  uploadImage: function (photo_group, img) {
    var that = this;
    wx.uploadFile({
      url: app.globalData.baseUrl + '/api/photo-items',
      method: 'POST',
      filePath: img.src,
      header: {
        'content-type': 'multipart/form-data'
      },
      name: 'file',
      formData: {
        group_id: photo_group.id,
        album_id: photo_group.album_id
      },
      success: function (r) {

      },
      fail: function (r) {

      }
    })

    console.log("upload photo:", photo_group)
  },

  bindPickerChange: function (e) {
    this.setData({
      albumIndex: e.detail.value
    })
  },
})
