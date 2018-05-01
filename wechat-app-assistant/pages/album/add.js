// pages/album/add.js
var app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {

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
   * 提交表单
   */
  formSubmit: function (e) {
    var that = this;
    var name = e.detail.value.name;

    wx.showLoading({ title: '提交中' });

    wx.request({
      method: 'POST',
      data: {
        name: name
      },
      url: app.globalData.baseUrl + '/api/albums',
      header: {
        'content-type': 'application/json'
      },
      success: function (res) {
        wx.hideLoading();
        wx.navigateTo({
          url: '/pages/album/list',
        })
      }
    });
  }
})
