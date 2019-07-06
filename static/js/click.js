layui.use('jquery', function(){
				var $ = layui.$;
		 
				//演示动画
				$('.site-doc-icon .layui-anim').on('click', function(){
					var othis = $(this), anim = othis.data('anim');
		 
					//停止循环
					if(othis.hasClass('layui-anim-loop')){
						return othis.removeClass(anim);
					}
		 
					othis.removeClass(anim);
		 
					setTimeout(function(){
						othis.addClass(anim);
					});
					//恢复渐隐
					if(anim === 'layui-anim-fadeout'){
						setTimeout(function(){
							othis.removeClass(anim);
						}, 1300);
					}
				});
			});