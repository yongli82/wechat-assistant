// pages/photo/add-video.js
var app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    video: false,
    size: 0,
    albumIndex: -1,
    albums: []
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

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
        that.setData({
          albums: res.data
        });
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
   * 选择 / 拍摄视频
   * @author abei<abei@nai8.me>
   */
  addVideo: function () {
    var that = this
    wx.chooseVideo({
      sourceType: ['album', 'camera'],
      maxDuration: 60,
      camera: 'back',
      success: function (res) {
        that.setData({
          video: res.tempFilePath,
          size: (res.size / (1024 * 1024)).toFixed(2)
        })
      }
    })
  },

  formSubmit: function (e) {
    var that = this;
    var desc = e.detail.value.desc;
    if (that.data.albumIndex < 0) {
      wx.showModal({
        title: app.globalData.appName,
        content: '请选择相册'
      })
      return false;
    }
    var albumId = that.data.albums[that.data.albumIndex].id;

    if (that.data.video == false) {
      wx.showModal({
        title: app.globalData.appName,
        content: '请录制或选择一个小视频'
      })
      return false;
    }

    if (that.data.size > 1024 * 1024 * 2) {
      wx.showModal({
        title: app.globalData.appName,
        content: '很抱歉，视频最大允许2M，当前为' + (that.data.size / (1024 * 1024)).toFixed(2) + 'M'
      })
      return false;
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
          var photo_group = res.data;
          wx.showLoading({ title: '视频上传中' });
          wx.uploadFile({
            url: app.globalData.baseUrl + '/api/video-items',
            method: 'POST',
            filePath: that.data.video,
            header: {
              'content-type': 'multipart/form-data'
            },
            name: 'file',
            formData: {
              photo_group: photo_group.id,
              album_id: photo_group.album_id
            },
            success: function (r) {
              wx.hideLoading();
              wx.showModal({
                title: app.globalData.appName,
                content: '上传成功',
              })
            },
            fail: function (r) {

            }
          })
        }
      }
    });
  },

  bindPickerChange: function (e) {
    this.setData({
      albumIndex: e.detail.value
    })
  },
})
