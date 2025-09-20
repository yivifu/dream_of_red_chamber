function handleResizeAndLoad(elements) {
	elements.forEach(el => {
		const containerWidth = el.parentElement.clientWidth; // 获取容器宽度
		const text = el.innerText;
		const fontSize = parseFloat(window.getComputedStyle(el).fontSize); // 获取字体大小
		const maxCharsTwoLine = 2 * Math.floor(containerWidth / (fontSize * 0.8)); // 计算两行文字合计最大字符数，0.8为样式中设置的字体大小的em值
		if (text.length > maxCharsTwoLine) {//文本长度大于即两行文字时
			// 分割文本
			let firstPart = text.slice(0, maxCharsTwoLine);
			let remainingPart = text.slice(maxCharsTwoLine);

			// 将首行加入双行合一的结构
			el.innerHTML = `<span>${firstPart}`;
			//剩余文本长度大于大于每行字符数时继续分割文本，将分割出的行加入双行合一的结构
			while (remainingPart.length > maxCharsTwoLine) {
				firstPart = remainingPart.slice(0, maxCharsTwoLine);
				remainingPart = remainingPart.slice(maxCharsTwoLine);
				el.innerHTML = ` ${el.innerHTML} <br/>${firstPart}`;
			}
			//将最后剩余的文本加入双行合一的结构
			el.innerHTML = `${el.innerHTML}<br/>${remainingPart}</span>`;
		} else {//文本长度小于每行最大字符数，直接将文本分割为长度相等的两行进行排版
			el.innerHTML = `<span>${text.slice(0, Math.ceil(text.length / 2))}<br/>${text.slice(Math.ceil(text.length / 2))}</span>`;
		}
		el.classList.add('double-line'); // 应用双行合一样式
	});
}
function handleResizeAndLoad1(elements) {
 elements.forEach(el => {
  const containerWidth = el.parentElement.clientWidth;
  const text = el.innerText;
  const fontSize = parseFloat(window.getComputedStyle(el).fontSize);
  const maxCharsTwoLine = 2 * Math.floor(containerWidth / (fontSize * 0.8));
  let lines = [];

  if (text.length > maxCharsTwoLine) {
   let remaining = text;
   while (remaining.length > maxCharsTwoLine) {
    lines.push(remaining.slice(0, maxCharsTwoLine));
    remaining = remaining.slice(maxCharsTwoLine);
   }
   if (remaining.length) lines.push(remaining);
  } else {
   const mid = Math.ceil(text.length / 2);
   lines = [text.slice(0, mid), text.slice(mid)];
  }

  // 清空原内容
  el.textContent = '';
  const span = document.createElement('span');
  lines.forEach((line, idx) => {
   if (idx > 0) span.appendChild(document.createElement('br'));
   span.appendChild(document.createTextNode(line));
  });
  el.appendChild(span);
  el.classList.add('double-line');
 });
}
document.addEventListener("DOMContentLoaded", function() {
	const elements = document.querySelectorAll('.adaptive-double-line');
	handleResizeAndLoad(elements);

	const noteDiv = document.getElementById('note');

	// 监听所有注释引用
	document.querySelectorAll('a[epub\\:type="noteref"]').forEach(function(el) {
		el.addEventListener('click', function(e) {
			e.preventDefault();
			e.stopPropagation();
			// 获取 href（如 #ch002note01），去掉 #
			const targetId = el.getAttribute('href').replace(/^#/, '');
			// 查找对应 aside
			const aside = document.getElementById(targetId);
			if (aside && noteDiv) {
				noteDiv.innerHTML = `<div class="note-content">${aside.innerHTML}</div>`;
				noteDiv.style.display = 'flex';
			}
		});
	});

	if(noteDiv){
	// 只监听noteDiv的点击
	    noteDiv.addEventListener('click', function (e) {
	        // 如果点击在.note-content外部，则关闭
	        if (!e.target.closest('.note-content')) {
	            noteDiv.style.display = 'none';
	            noteDiv.innerHTML = '';
	        }
	    });
	}
});
//窗口宽度调整时重新计算并设置双行合一
window.addEventListener('resize', function() {
	const elements = document.querySelectorAll('.adaptive-double-line');
	handleResizeAndLoad(elements);
});