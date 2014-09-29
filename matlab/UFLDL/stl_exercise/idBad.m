index = 0;
toView = zeros(784,100);
for n=1:15298
	if pred(n) ~= testLabels(n)
		index = index+1;
		disp(sprintf('%d %d %d %d', index, n, pred(n), trainLabels(n)));
		toView(:,index) = testData(:,n);
%		if index >= 100
%			break;
%		end
	end
end
display_network(toView);