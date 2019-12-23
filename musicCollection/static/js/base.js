    function searchkeyword(page=1){
        var arts = new Array(),gens = new Array(),yrs = new Array();
        var allart=false,allgen=false,allyr=false;
        // retain the checked status of each metadata category
        $('.nav-link-cb').each(function(i,e){
            var ischecked = $(this).prop("checked");
            var linktext = $(this).siblings('.link-text').text().toLowerCase()
            if (linktext=="artists") {
                allart = ischecked?true:false;
            }
            if (linktext=="genres") {
                allgen = ischecked?true:false;
            }
            if (linktext=="years") {
                allyr = ischecked?true:false;
            }
        });
        // find all the checked checkboxes and form the list of arts, gens, yrs
        $('.my-cb').each(function(i,e){
            var ischecked = $(this).prop("checked");
            if (ischecked==true) {
                var linktext = $(this).parents('.nav-items').siblings('.nav-link').children('.link-text').text().toLowerCase()
                var itemtext = $(this).siblings('.nav-item-lb').text()
                if (linktext=="artists") {
                    arts.push(itemtext);
                }else if(linktext=="genres"){
                    gens.push(itemtext);
                }else if(linktext=="years"){
                    yrs.push(itemtext);
                }
            }
        });

        var upload_data = {"keyword":$('.searchMetadata').val(),"arts":JSON.stringify(arts),
                "gens":JSON.stringify(gens),"yrs":JSON.stringify(yrs),"page":page};
        $.post({
            url:"/searchkeyword",
            data:upload_data,   
            dataType:'json',
            success:function(data){
                formResultandFacet(data);
                retainCheck(data,arts,gens,yrs,allart,allgen,allyr);
            }
        });
    }

    var formResultandFacet = function(data){
        formResult(data);
        formFacet(data);
    }

    var formResult = function(data){
        $('.result-item').remove();
        songlist = data.result_list
        for (i in songlist){
            var liitem = $("<li class='result-item row'></li>")
            var metaData = $("<div class='col-md-7'></div>")
            var title = songlist[i].title
            var artist = songlist[i].artist
            var album = songlist[i].album
            var genre = songlist[i].genre
            var year = songlist[i].year
            var duration = songlist[i].duration
            var download_url = songlist[i].download_url
            var picsrc = songlist[i].pic_src

            if(picsrc!=null){
                var pic = $("<div class='col-md-3'><a href="+download_url+"><img src='"+picsrc+"'/><div class='play'><i class='fas fa-play-circle fa-3x'></i></div></a></div>")
            }else{
                var pic = $("<div class='col-md-3'><a href="+download_url+"><span class='fas fa-headphones fa-6x' aria-hidden='true'></span><div class='play'><i class='fas fa-play-circle fa-3x'></i></div></a></div>")
            }

            var div_result1 = $("<div class='result-text'><p>Title:</p>"+title+"</div>")
            var div_result2 = $("<div class='result-text'><p>Artist:</p>"+artist+"</div>")
            var div_result3 = $("<div class='result-text'><p>Album:</p>"+album+"</div>")
            var div_result4 = $("<div class='result-text'><p>Genre:</p>"+genre+"</div>")
            var div_result5 = $("<div class='result-text'><p>Year:</p>"+year+"</div>")
            var div_result6 = $("<div class='result-text'><p>Duration:</p>"+duration+"</div>")
            metaData.append(div_result1)
            metaData.append(div_result2)
            metaData.append(div_result3)
            metaData.append(div_result4)
            metaData.append(div_result5)
            metaData.append(div_result6)
            liitem.append(pic)
            liitem.append(metaData)

            $('.results').append(liitem);
        }
        doPagination(data); // form the pagination div part regarding the result
    };

    function formFacet(data){
        $('.nav-result-item').remove();

        // get top 5 artists in the search results
        artists = eval(data.alist)
        for(i in artists){
            var liitem = $("<li class='nav-result-item'></li>")

            var name = artists[i][0]
            var count = artists[i][1]

            var div_result=$("<div><input type='checkbox' class='my-cb' onchange='changeCheck(this)'>"+
                "<i class='far fa-square'></i><label class='nav-item-lb'>"+name+"</label><p>("+count+")</p></div>");
            liitem.append(div_result)
            $('.side-nav:nth-child(1) .nav-items').append(liitem)
        }

        // get top 5 genres in the search results
        genres = eval(data.glist)
        for(i in genres){
            var liitem = $("<li class='nav-result-item'></li>")

            var name = genres[i][0]
            var count = genres[i][1]

            var div_result=$("<div><input type='checkbox' class='my-cb' onchange='changeCheck(this)'>"+
                "<i class='far fa-square'></i><label class='nav-item-lb'>"+name+"</label><p>("+count+")</p></div>");
            liitem.append(div_result)
            $('.side-nav:nth-child(2) .nav-items').append(liitem)
        }

        // get top 5 years in the search results  
        years = eval(data.ylist)  
        for(i in years){
            var liitem = $("<li class='nav-result-item'></li>")

            var name = years[i][0]
            var count = years[i][1]

            var div_result=$("<div><input type='checkbox' class='my-cb' onchange='changeCheck(this)'>"+
                "<i class='far fa-square'></i><label class='nav-item-lb'>"+name+"</label><p>("+count+")</p></div>");
            liitem.append(div_result)
            $('.side-nav:nth-child(3) .nav-items').append(liitem)
        } 
    }

    function retainCheck(data,arts,gens,yrs,allart,allgen,allyr){
        if (allart) { $('.side-nav:nth-child(1) .fa-square').attr('class','far fa-check-square')}
        if (allgen) { $('.side-nav:nth-child(2) .fa-square').attr('class','far fa-check-square')}
        if (allyr) { $('.side-nav:nth-child(3) .fa-square').attr('class','far fa-check-square')}
        if(arts.length>0){
            retainEachCheck(arts, 1)
        }
        if(gens.length>0){
            retainEachCheck(gens, 2)
        }
        if(yrs.length>0){
            retainEachCheck(yrs, 3)
        }
    }

    function retainEachCheck(obj, index){
        for(i in obj){
                $('.side-nav:nth-child('+index+') .nav-item-lb').each(function(){
                    if (obj[i]==$(this).text()) {
                        $(this).siblings('.fa-square').attr('class','far fa-check-square')
                        $(this).siblings('.my-cb').prop('checked',true)
                    }
                })
        }
        var rlt_ct = $('.side-nav:nth-child('+index+') .nav-item-lb').parents('.nav-result-item').length
        if (rlt_ct==obj.length) {
            $('.side-nav:nth-child('+index+') .fa-square').attr('class','far fa-check-square')
            $('.side-nav:nth-child('+index+') .nav-link-cb').prop('checked',true)
        }
    }

    function doPagination(data){
        var page = data.page
        var count = data.count
        var total = data.total
        var show_first_page = data.show_first_page
        var page_list = data.page_list
        $('.page').append('<ul class="pagination col-md-9 justify-content-center"></ul>')
        var page_rlt = $('.pagination')

        $('.page-item').remove();

        var fst = $('<li class="page-item fst" onclick="goToPage($(this))"><span class="page-link" aria-hidden="1"><p>&laquo;</p></span></li>')
        var prv = $('<li class="page-item prv" onclick="goToPage($(this))"><span class="page-link" aria-hidden="'+(page-1)+'"><p>&lt;</p></span></li>')
        page_rlt.append(fst)
        page_rlt.append(prv)
        if (show_first_page!=1){
            $('.fst').addClass("disabled")
            $('.fst a').attr("tabindex","-1")
            $('.prv').addClass("disabled")
            $('.prv a').attr("tabindex","-1")
        }

        for (i in page_list) {
            if(page_list[i]==page){
                var active_pg = $('<li class="page-item active" onclick="goToPage($(this))"><span class="page-link" aria-hidden="'+page_list[i]+'">'+page_list[i]+'</span></li>')
                page_rlt.append(active_pg)
            }else{
                var pg = $('<li class="page-item" onclick="goToPage($(this))"><span class="page-link" aria-hidden="'+page_list[i]+'">'+page_list[i]+'</span></li>')
                page_rlt.append(pg)
            }
        }

        var nxt = $('<li class="page-item nxt" onclick="goToPage($(this))"><span class="page-link" aria-hidden="'+(page+1)+'"><p>&gt;</p></span></li>')
        var lst = $('<li class="page-item lst" onclick="goToPage($(this))"><span class="page-link" aria-hidden="'+total+'"><p>&raquo;</p></span></li>')
        page_rlt.append(nxt)
        page_rlt.append(lst)
        if (page >= total) {
            $('.nxt').addClass("disabled")
            $('.nxt a').attr("tabindex","-1")
            $('.lst').addClass("disabled")
            $('.lst a').attr("tabindex","-1")
        }
        $('.page').append('<div class="tot_result col-md-3 text-center bg-transparent"></div>')
        var last = page*10;
        if (page==total & count< page*10) {
            last = count
        }
        $('.tot_result').text('Results '+(page*10-9)+' to '+last+' of '+count)
    }

    function goToPage(obj){
        var cur_page = obj.children('span').attr('aria-hidden')
        searchkeyword(cur_page)
        $('html , body').animate({scrollTop: 0},'slow'); // go back to top
    }

    function selectAll(){
        $('.nav-link-cb').each(function(i,e){
            $(this).change(function(){
                var ischecked = $(this).prop("checked");
                if(ischecked==true){
                    var svgnt = $(this).siblings('.fa-square')
                    svgnt.attr('class','far fa-check-square')
                }else{
                    var svgnt = $(this).siblings('.fa-check-square')
                    svgnt.attr('class','far fa-square')
                }
                var children_cb = $(this).parents().siblings('.nav-items').children().children().children('input');
                children_cb.prop("checked",ischecked);
                changeCheck(children_cb);
            });
        });
    }

    function changeCheck(obj){
        var cb = $(obj)
        var ischecked = cb.prop("checked");
        console.log(obj,ischecked)
        if(ischecked==true){
            var svgnt = $(this).siblings('.fa-square')
            svgnt.attr('class','far fa-check-square')
        }else{
            var svgnt = $(this).siblings('.fa-check-square')
            svgnt.attr('class','far fa-square')
        }
        searchkeyword();
    }

    function listenToggleNavBtn(){
        $('.navbar-toggler').click(function(){
            var iscollapsed = $('.navbar-collapse').hasClass('show')
            if (iscollapsed) {
                $('.sidebar').attr('class','col-md-3 d-md-block sidebar collapsed')
                $('.wrapper').addClass('collapsed')
            }else{
                $('.sidebar').attr('class','col-md-3 d-md-block sidebar')
                $('.wrapper').removeClass('collapsed')
            }
        })
    }


    $(function(){
        searchkeyword();
        selectAll(); // select or unselect all the children checkboxes
        listenToggleNavBtn(); // when meadia width less than 768px, only show side bar when navbar not collapsed
        
        $('.searchMetadata').keydown(function(e){
            if (e.keyCode=='13') {
                searchkeyword();
                $('.nav-link-cb').prop("checked",false);
                $('.my-cb').prop("checked",false);
            }
      });


    });
